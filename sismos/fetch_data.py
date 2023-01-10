"""
fetch_data.py

This is the script to fetch more data from the INETER's "API".
"""
from sismos import database, models
from sismos.ineter import get_data_from_api

models.Base.metadata.create_all(bind=database.engine)

db = database.SessionLocal()  # pylint: disable=invalid-name


def fetch_sismos():
    """
    Fetch sismos from INETER's API, adding new ones if found!
    """
    data = get_data_from_api()

    for sismo in data:
        if (
            not db.query(models.Sismo)
            .filter_by(content_hash=sismo["content_hash"])
            .first()
        ):
            db.add(sismo)
        elif (
            db_sismo := db.query(models.Sismo)
            .filter_by(partial_content_hash=sismo["partial_content_hash"])
            .first()
        ):
            db_sismo.created = sismo["created"]
            db_sismo.lat = sismo["lat"]
            db_sismo.long = sismo["long"]
            db_sismo.depth = sismo["depth"]
            db_sismo.richter = sismo["richter"]
            db_sismo.description = sismo["description"]
            db_sismo.location = sismo["location"]
            db_sismo.country = sismo["country"]
            db_sismo.content_hash = sismo["content_hash"]
            db_sismo.partial_content_hash = sismo["partial_content_hash"]

            db.add(db_sismo)
        else:
            continue

        db.commit()


def main():  # pylint: disable=missing-function-docstring
    fetch_sismos()


if __name__ == "__main__":
    main()
