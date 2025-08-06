"""SQLAlchemy model for the items table."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Text, BigInteger
from sqlalchemy.sql import func

from ..core.db import Base


class Item(Base):
    """Represents an item stored in the database."""

    __tablename__ = "items"

    id: int = Column(BigInteger, primary_key=True, index=True)
    name: str = Column(Text, nullable=False)
    created_at: datetime = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def to_dict(self) -> dict:
        """Return a dictionary representation of the item."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
