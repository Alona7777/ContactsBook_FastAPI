from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Date, Integer, ForeignKey, DateTime, func


class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(15), index=True)
    last_name: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    phone: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    birth_date: Mapped[Date] = mapped_column(Date)
    info: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped[Date] = mapped_column('created_at', DateTime, default=func.now(), nullable=True)
    updated_at: Mapped[Date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now(), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', nullable=True))
    user: Mapped['User'] = relationship('User', backref='contacts', lazy='joined')



class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(15), index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[Date] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[Date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now())


