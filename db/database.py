from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base


class Database:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()

