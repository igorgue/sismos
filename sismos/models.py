"""
models.py

This is the models file for the Sismos API.
"""

from sqlalchemy import Column, DateTime, Float, Integer, String

from .database import Base


class Sismo(Base):  # pylint: disable=too-few-public-methods
    """
    This is the Sismo model.
    """

    __tablename__ = "sismos"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, index=True)
    lat = Column(Float, index=True)
    long = Column(Float, index=True)
    depth = Column(Float, index=True)
    richter = Column(Float, index=True)
    description = Column(String, index=True)
    location = Column(String, index=True)

    content_hash = Column(String, unique=True, index=True)
