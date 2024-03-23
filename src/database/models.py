from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Date, Integer, ForeignKey


class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(15), index=True)
    last_name: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    birth_date: Mapped[Date] = mapped_column(Date)
    info: Mapped[str] = mapped_column(String(100), nullable=True)


class PhoneNumber(Base):
    __tablename__ = 'phones'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)

class ContactPhone(Base):
    __tablename__ = 'contacts_phons'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contact_id: Mapped[int] = mapped_column(Integer, ForeignKey('contacts.id', ondelete='CASCADE'), nullable=False)
    phone_id: Mapped[list] = mapped_column(Integer, ForeignKey('phones.id', ondelete='CASCADE'), nullable=False)
