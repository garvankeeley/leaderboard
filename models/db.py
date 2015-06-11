from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.reflection import Inspector

class DB(object):
    instance = None

    def __init__(self):
        print 'setup db'
        self.engine = create_engine('postgresql+pg8000://localhost', echo=True)
        self.Base = declarative_base(self.engine)
        self.metadata = self.Base.metadata
        db_session = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.session = db_session()

    def table_exists(self, name):
        inspector = Inspector.from_engine(get_db().engine)
        return name in inspector.get_table_names()

    def commit(self):
        self.session.commit()

def get_db():
    """
    :rtype: DB
    """
    if not DB.instance:
        DB.instance = DB()
    return DB.instance
