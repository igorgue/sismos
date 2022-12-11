"""
fetch_initial_data.py

This is the script to fetch the initial data from the INETER's "API".
so when we start the api we have some data to work with.
"""
from sismos import database, models
from sismos.ineter import get_data_from_api
from sismos.location import NICARAGUAN_STATES

models.Base.metadata.create_all(bind=database.engine)

db = database.SessionLocal()  # pylint: disable=invalid-name


def fetch_sismos():
    """
    Fetch the sismos from the INETER's API.
    """
    if db.query(models.Sismo).first() is not None:
        print("The database already has items, skipping...")

        return

    data = get_data_from_api()

    print(f"Adding {len(data)} sismos to the database.")

    models.Sismo.create_from(db, data)


def create_locations():
    """
    Create the locations for the sismos.
    """
    if db.query(models.Location).first() is not None:
        print("The database already has items, skipping...")

        return

    for name, lat_long in NICARAGUAN_STATES.items():
        location = models.Location(
            name=name.title(),
            latitude=lat_long[0],
            longitude=lat_long[1],
        )

        db.add(location)

    db.commit()


def main():
    """
    Main function.
    """
    fetch_sismos()
    create_locations()


if __name__ == "__main__":
    main()
