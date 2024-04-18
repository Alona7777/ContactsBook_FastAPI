import unittest
from unittest.mock import MagicMock, AsyncMock

from datetime import date, timedelta
from sqlalchemy.orm import Session

from src.schemas.contacts import ContactResponse, ContactBase
from src.schemas.user import UserBase, UserResponse
from src.database.models import User, Contact
from src.repository.contacts import get_contacts, search_contacts, get_upcoming_birthdays_contacts
from src.repository.full_access import get_all_contacts
from src.repository.one_contact import get_contact, get_contact_by_email, create_contact, update_contact, update_email, update_info, update_last_name, update_name, update_phone, remove_contact
from src.repository.users import get_user_by_email, create_user, update_avatar_url, update_token, confirmed_email


class TestAsyncContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.user = User(id=1, username='test_user', password='qwerty', confirmed=True)
        self.session = MagicMock(spec=Session)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_search_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await search_contacts(query='query', user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_upcoming_birthdays_contacts(self):
        contacts = [Contact(birth_date=date.today() + timedelta(days=3)), 
                    Contact(birth_date=date.today() + timedelta(days=10))] 
        self.session.query().filter().all.return_value = contacts
        result = await get_upcoming_birthdays_contacts(user=self.user, db=self.session)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].birth_date, date.today() + timedelta(days=3))

    async def test_get_all_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().offset().limit().all.return_value = contacts
        result = await get_all_contacts(skip=0, limit=10, db=self.session)
        self.assertEqual(result, contacts)


class TestAsyncContact(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.user = User(id=1, username='test_user', password='qwerty', confirmed=True)
        self.session = MagicMock(spec=Session)

    async def test_get_contact(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=contact.id, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_by_email(self):
        contact = Contact(first_name='test', 
                           last_name='test', 
                           email='user@example.com', 
                           phone='12123456789', 
                           birth_date=date.today(), 
                           info='test')
        self.session.query().filter().first.return_value = contact
        result = await get_contact_by_email(contact_email='user@example.com', user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_create_contact(self):
        body = ContactBase(first_name='test', 
                           last_name='test', 
                           email='user@example.com', 
                           phone='12123456789', 
                           birth_date=date.today(), 
                           info='test')
        result = await create_contact(body=body, db=self.session, user=self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birth_date, body.birth_date)
        self.assertEqual(result.info, body.info)

    async def test_update_contact(self):
        contact = Contact()
        body = ContactBase(first_name='test', 
                           last_name='test', 
                           email='user@example.com', 
                           phone='12123456789', 
                           birth_date=date.today(), 
                           info='test')
        self.session.query().filter().first.return_value = contact
        result = await update_contact(contact_id=contact.id, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_name(self):
        contact = Contact()
        name = 'test_test'
        self.session.query().filter().first.return_value = contact
        result = await update_name(contact_id=contact.id, first_name=name, user=self.user, db=self.session)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.first_name[0], name)

    async def test_update_last_name(self):
        contact = Contact()
        last_name = 'test_test'
        self.session.query().filter().first.return_value = contact
        result = await update_last_name(contact_id=contact.id, last_name=last_name, user=self.user, db=self.session)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.last_name[0], last_name)   

    async def test_update_email(self):
        contact = Contact()
        email = 'test_email'
        self.session.query().filter().first.return_value = contact
        result = await update_email(contact_id=contact.id, email=email, user=self.user, db=self.session)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.email[0], email)

    async def test_update_phone(self):
        contact = Contact()
        phone = '12123456789'
        self.session.query().filter().first.return_value = contact
        result = await update_phone(contact_id=contact.id, phone=phone, user=self.user, db=self.session)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.phone[0], phone)

    async def test_update_info(self):
        contact = Contact()
        info = 'test_info'
        self.session.query().filter().first.return_value = contact
        result = await update_info(contact_id=contact.id, info=info, user=self.user, db=self.session)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.info[0], info)

    async def test_remove_contact(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=contact.id, user=self.user, db=self.session)
        self.assertEqual(result, contact)


class TestAsyncUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.user = User()
        self.session = MagicMock(spec=Session)

    async def test_get_user_by_email(self):
        self.session.query().filter().first.return_value = self.user
        result = await get_user_by_email(email='user@example.com', db=self.session)
        self.assertEqual(result, self.user)

    async def test_update_token(self):
        token = 'test'
        result = await update_token(user=self.user, token=token, db=self.session)
        self.assertEqual(self.user.refresh_token, token)
    
    async def test_confirmed_email(self):
        self.session.query().filter().first.return_value = self.user
        result = await confirmed_email(email='user@example.com', db=self.session)
        self.assertEqual(self.user.confirmed, True)
    
    async def test_update_avatar_url(self):
        url = 'test'
        self.session.query().filter().first.return_value = self.user
        result = await update_avatar_url(email='user@example.com', url=url, db=self.session)
        self.assertIsInstance(result, User)
        self.assertEqual(result.avatar, url)   

    async def test_create_user(self):
        body = UserBase(username='test', 
                        email='user@example.com',
                        password='12345678')
        result = await create_user(body=body, db=self.session)
        self.assertIsInstance(result, User)

