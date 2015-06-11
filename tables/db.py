from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.reflection import Inspector

class DB:
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

def get_db():
    if not DB.instance:
        DB.instance = DB()
    return DB.instance
