import redis
import pickle
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.conf.config import config


class Auth:
    """
    A class containing methods for authentication and authorization.

    Attributes:
        pwd_context (CryptContext): An instance of CryptContext for password hashing.
        SECRET_KEY (str): Secret key used for JWT encoding and decoding.
        ALGORITHM (str): Algorithm used for JWT encoding and decoding.
        oauth2_scheme (OAuth2PasswordBearer): An instance of OAuth2PasswordBearer for token authentication.
        cache (Redis): An instance of Redis for caching user data.

    Methods:
        verify_password: Verify if a plain password matches a hashed password.
        get_password_hash: Get the hashed version of a password.
        create_access_token: Create an access token for a user.
        create_refresh_token: Create a refresh token for a user.
        decode_refresh_token: Decode a refresh token and extract the email address.
        get_current_user: Get the current authenticated user from the token.
        create_email_token: Create a token for email verification.
        get_email_from_token: Get the email address from an email verification token.
    """
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    SECRET_KEY = config.SECRET_KEY
    ALGORITHM = config.ALGORITHM
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/auth/login')
    cache = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=0,
        password=config.REDIS_PASSWORD,
    )

    def verify_password(self, plain_password, hashed_password):
        """
        The verify_password function takes a plain-text password and hashed
        password as arguments. It then uses the CryptContext instance to verify that
        the given plain-text password matches the given hashed_password.
        
        :param self: Represent the instance of the class
        :param plain_password: Store the password that is entered by the user
        :param hashed_password: Check if the password entered by the user matches with that in the database
        :return: True if the plain_password matches the hashed_password
        :doc-author: Trelent
        """
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str):
        """
        The get_password_hash function takes a password and returns the hashed version of it.
        The hashing algorithm is defined in the config file, which is imported into this module.
        
        :param self: Represent the instance of the class
        :param password: str: Get the password from the user
        :return: A string that is a hash of the password
        :doc-author: Trelent
        """
        return self.pwd_context.hash(password)
    
    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_access_token function creates a new access token for the user.
            The function takes in two parameters: data and expires_delta.
            Data is a dictionary that contains information about the user, such as their username and password.
            Expires_delta is an optional parameter that specifies how long the access token will be valid for.
        
        :param self: Refer to the current instance of a class
        :param data: dict: Pass in the data that will be encoded into the jwt
        :param expires_delta: Optional[float]: Set the expiration time for the access token
        :return: A string, which is the encoded access token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({'iat': datetime.utcnow(), 'exp': expire, 'scope': 'access_token'})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token
    
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_refresh_token function creates a refresh token for the user.
            The function takes in two parameters: data and expires_delta.
            Data is a dictionary containing the user's id, username, email address, and password hash.
            Expires_delta is an optional parameter that determines how long the refresh token will be valid for.
        
        :param self: Represent the instance of the class
        :param data: dict: Pass the user_id to the function
        :param expires_delta: Optional[float]: Set the expiration time of the refresh token
        :return: A refresh token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({'iat': datetime.utcnow(), 'exp': expire, 'scope': 'refresh_token'})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token
    
    async def decode_refresh_token(self, refresh_token: str):
        """
        The decode_refresh_token function takes a refresh token and decodes it.
        If the scope is 'refresh_token', then the email address of the user is returned.
        Otherwise, an HTTPException with status code 401 (Unauthorized) is raised.
        
        :param self: Represent the instance of a class
        :param refresh_token: str: Pass the refresh token to be decoded
        :return: The email of the user
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
    
    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        The get_current_user function is a dependency that will be used in the
            get_current_active_user endpoint. It takes in a token and db session,
            verifies the token, and returns an active user object from the database.
        
        :param self: Access the class attributes
        :param token: str: Get the token from the authorization header
        :param db: Session: Access the database
        :return: The user object that is associated with the email address
        :doc-author: Trelent
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload['sub']
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception
        
        user_hash = str(email)
        user = self.cache.get(user_hash)
        if user is None:
            user = await repository_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            self.cache.set(user_hash, pickle.dumps(user))
            self.cache.expire(user_hash, 300)
        else:
            user = pickle.loads(user)
        return user
    
    def create_email_token(self, data: dict):
        """
        The create_email_token function creates a token that is used to verify the user's email address.
        The token is created using the JWT library and contains information about when it was issued,
        when it expires, and what data should be encoded into the token. The function returns this 
        token as a string.
        
        :param self: Represent the instance of the class
        :param data: dict: Pass in the data to be encoded
        :return: A token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({'iat': datetime.utcnow(), 'exp': expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token
    
    async def get_email_from_token(self, token: str):
        """
        The get_email_from_token function takes a token as an argument and returns the email address associated with that token.
        If the token is invalid, it raises an HTTPException.
        
        :param self: Represent the instance of the class
        :param token: str: Pass the token to the function
        :return: The email address of the user
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload['sub']
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail='Invalid token for email verification')

auth_service = Auth()






