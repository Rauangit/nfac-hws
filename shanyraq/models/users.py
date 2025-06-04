from sqlalchemy import String, func, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from database import Base
from datetime import datetime


class Account(Base):
    __tablename__ = "accounts"

    account_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email_address: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    user_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)

    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Account id={self.account_id} user_name={self.user_name} email={self.email_address}>"
