import pytest
from fastapi.testclient import TestClient
from httpx import WSGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import MagicMock, patch
from main import app
from src.database.models import Base, User
from src.database.db import get_db
from src.services.auth import auth_service


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

test_user = {
    "username": "deadpool",
    "email": "deadpool@example.com",
    "password": "12345678",
}


# @pytest.fixture(scope="module", autouse=True)
# def init_models_wrap():
#     async def init_models():
#         async with engine.begin() as conn:
#             await conn.run_sync(Base.metadata.drop_all)
#             await conn.run_sync(Base.metadata.create_all)
#         async with TestingSessionLocal() as session:
#             hash_password = auth_service.get_password_hash(test_user["password"])
#             current_user = User(username=test_user["username"], email=test_user["email"], password=hash_password,
#                                 confirmed=True, role="admin")
#             session.add(current_user)
#             await session.commit()

#     asyncio.run(init_models())


@pytest.fixture(scope="module", autouse=True)
def session():
    # Create the database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# @pytest.fixture(scope="module", autouse=True)
# def client(session):
#     # Dependency override

#     def override_get_db():
#         try:
#             yield session
#         # except Exception as err:
#         #     print(err)
#         #     session.rollback()
#         finally:
#             session.close()

#     app.dependency_overrides[get_db] = override_get_db
#     transport = WSGITransport(app=app)
#     yield TestClient(app, base_url="http://testserver")

@pytest.fixture(scope="module", autouse=True)
def client(session):
    # Создаем клиента с правильными зависимостями
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    # Создаем тестового клиента
    with TestClient(app, base_url="http://testserver") as client:
        yield client



@pytest.fixture(scope="module")
def user():
    return {
        "username": "deadpool",
        "email": "deadpool@example.com",
        "password": "12345678",
    }

@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = (
        session.query(User).filter(User.email == user.get("email")).first()
    )
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )
    data = response.json()
    return data["access_token"]

