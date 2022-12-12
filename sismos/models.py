"""
models.py

This is the models file for the Sismos API.
"""
from datetime import datetime

import pytz
from sqlalchemy import Column, DateTime, Float, Integer, String, desc, insert
from sqlalchemy.orm import Query, Session

from .database import Base

timezone = pytz.timezone("America/Managua")


def exec_generic_statement(
    db: Session, sql_stmt: str  # pylint: disable=invalid-name
) -> str:
    """
    Execute a count statement.
    """
    result = db.execute(sql_stmt).fetchall()

    if not result:
        return "?"

    return "\n".join(str(item) for item in result)


class Location(Base):  # pylint: disable=too-few-public-methods
    """
    Location model.
    """

    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    created = Column(DateTime)
    name = Column(String, unique=True)
    lat = Column(Float)
    long = Column(Float)

    @classmethod
    def create_from(cls, db: Session, data: dict):  # pylint: disable=invalid-name
        """
        Create a location from a dictionary.
        """

        for state, (lat, long) in data.items():
            db.add(
                cls(
                    created=datetime.now(timezone),
                    name=state,
                    lat=lat,
                    long=long,
                )
            )
        db.commit()

    @classmethod
    def get_coordinates(cls, db: Session, state: str):  # pylint: disable=invalid-name
        """
        Get the coordinates for a state.
        """
        return db.query(cls.lat, cls.long).filter(cls.name == state).first()


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
    def exec_select_statement(
        cls, db: Session, sql_stmt: str  # pylint: disable=invalid-name
    ) -> list["Sismo"]:
        """
        Execute the query.
        """
        result = db.execute(sql_stmt)

        data = result.all()

        ids = [row[0] for row in data]

        return cls.ordered(db).filter(cls.id.in_(ids)).all()

    @classmethod
    def ordered(cls, db: Session) -> "Query['Sismo']":  # pylint: disable=invalid-name
        """
        Get the sismos ordered by created.
        """
        return db.query(cls).order_by(desc(cls.created))

    @classmethod
    def latest(
        cls, db: Session, limit: int = 5  # pylint: disable=invalid-name
    ) -> list["Sismo"]:
        """
        Get the last sismos.
        """
        return cls.ordered(db).limit(limit).all()

    @classmethod
    def create_from(cls, db: Session, data: list[dict]):  # pylint: disable=invalid-name
        """
        Create the sismos from the data.
        """
        stmt = insert(cls).prefix_with("OR IGNORE")

        for item in data:
            db.execute(stmt.values(**item))

        db.commit()

    @classmethod
    def clear(cls, db: Session):  # pylint: disable=invalid-name
        """
        Clear the sismos.
        """
        db.query(cls).delete()
        db.commit()
