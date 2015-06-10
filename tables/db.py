from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class DB:
    instance = None

    def __init__(self, is_test=False):
        print 'setup db'
        self.engine = create_engine('postgresql+pg8000://localhost', echo=True)
        self.Base = declarative_base(self.engine)
        self.metadata = self.Base.metadata
        db_session = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.session = db_session()

def get_db(is_test=False):
    if not DB.instance:
        DB.instance = DB(is_test)
    return DB.instance
