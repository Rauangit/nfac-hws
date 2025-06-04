from sqlalchemy import String, Integer, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime


class Advertisement(Base):
    __tablename__ = "advertisements"

    ad_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    headline: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=True)

    created_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return f"<Advertisement ad_id={self.ad_id} headline={self.headline} cost={self.cost}>"
