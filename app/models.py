from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from sqlalchemy import String

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
