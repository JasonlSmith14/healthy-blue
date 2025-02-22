from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base


class Database:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Creates tables in the database from the Base metadata"""
        Base.metadata.create_all(self.engine)
        print("Tables created successfully.")

    def get_session(self):
        """Returns a session object to interact with the database"""
        return self.Session()

    def drop_tables(self):
        """Drops all tables from the database"""
        Base.metadata.drop_all(self.engine)
        print("Tables dropped successfully.")
