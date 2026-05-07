from backend.db.database import engine, Base
from backend.db import models


def init_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database setup complete.")


if __name__ == "__main__":
    init_database()