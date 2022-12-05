"""
models.py

This is the models file for the Sismos API.
"""

from sqlalchemy import Column, DateTime, Float, Integer, String, insert
from sqlalchemy.orm import Session

from .database import Base


class Sismo(Base):  # pylint: disable=too-few-public-methods
    """
    This is the Sismo model.
    """

    __tablename__ = "sismos"

    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime, index=True)
    lat = Column(Float, index=True)
    long = Column(Float, index=True)
    depth = Column(Float, index=True)
    richter = Column(Float, index=True)
    description = Column(String, index=True)
    location = Column(String, index=True)
    country = Column(String, index=True)

    content_hash = Column(String, unique=True, index=True)

    @classmethod
    def latest(cls, limit: int = 5) -> list["Sismo"]:
        """
        Get the last sismos.
        """
        return cls.query(limit=limit).all()

    @classmethod
    def create_from(cls, db: Session, data: list[dict]):  # pylint: disable=invalid-name
        """
        Create the sismos from the data.
        """
        stmt = insert(cls).prefix_with("OR IGNORE")

        for item in data:
            db.execute(stmt.values(**item))

        db.commit()
