import enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Date, Integer, ForeignKey, DateTime, func, Enum, Boolean


class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(15), index=True)
    last_name: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    birth_date: Mapped[Date] = mapped_column(Date)
    info: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped[Date] = mapped_column(Date, default=func.now(), nullable=True)
    updated_at: Mapped[Date] = mapped_column(Date, default=func.now(), onupdate=func.now(), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    user: Mapped['User'] = relationship(backref='contact', lazy='joined')


class Role(enum.Enum):
    admin: str = 'admin'
    moderator: str = 'moderator'
    user: str = 'user'


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(15), index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[Date] = mapped_column(Date, default=func.now())
    updated_at: Mapped[Date] = mapped_column(Date, default=func.now(), onupdate=func.now())
    role: Mapped[Enum] = mapped_column(Enum(Role), default=Role.user)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)

