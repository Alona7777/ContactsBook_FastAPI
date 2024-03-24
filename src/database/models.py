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
    phone: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    birth_date: Mapped[Date] = mapped_column(Date)
    info: Mapped[str] = mapped_column(String(100), nullable=True)

