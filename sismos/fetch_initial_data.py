"""
fetch_initial_data.py

This is the script to fetch the initial data from the INETER's "API".
so when we start the api we have some data to work with.
"""
from sismos import database, models
from sismos.ineter import get_data_from_api

models.Base.metadata.create_all(bind=database.engine)

db = database.SessionLocal()  # pylint: disable=invalid-name

def main():
    """
    Main function.
    """
    if db.query(models.Sismo).first() is not None:
        print("The database already has items, skipping...")

        return

    data = get_data_from_api()

    print(f"Adding {len(data)} sismos to the database.")

    models.Sismo.create_from(db, data)


if __name__ == "__main__":
    main()
