from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.reflection import Inspector

import json
import pkgutil

class DB(object):
    instance = None

    def __init__(self):
        # Try to load the database connection from the configuration
        # in the package, otherwise just use default connection
        # params.
        json_data = pkgutil.get_data('leaderboard', 'db_connection_params.json')
        jdata = json.loads(json_data)

        conn_tmpl = 'postgresql+pg8000://%(user)s:%(password)s@localhost/%(database)s'
        conn_str = conn_tmpl % jdata
        self.engine = create_engine(conn_str, echo=True)

        self.Base = declarative_base(self.engine)
        db_session = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.session = db_session()

    def table_exists(self, name):
        inspector = Inspector.from_engine(get_db().engine)
        return name in inspector.get_table_names()

    def commit(self):
        self.session.commit()

    def add(self, obj):
        self.session.add(obj)

    def get_session(self):
        """
        :rtype: Session
        """
        return self.session

    def get_metadata(self):
        return self.Base.metadata

    def create_all(self):
        from leaderboard.models.country_bounds import CountryBounds
        from leaderboard.models.user import User
        from leaderboard.models.tile import Tile
        do_load = not self.table_exists(CountryBounds.__tablename__)
        self.get_metadata().create_all(self.engine)

        if do_load:
            CountryBounds.load_countries()

    def drop_all(self):
        # endure session is committed
        self.commit()
        from leaderboard.models.country_bounds import CountryBounds
        from leaderboard.models.user import User
        from leaderboard.models.tile import Tile
        from leaderboard.models.calendar_factory import get_current_week_table_class
        wk = get_current_week_table_class()
        if self.table_exists(wk.__tablename__):
            t = wk.__table__
            t.drop(get_db().engine)
        for tbl in reversed(get_db().get_metadata().sorted_tables):
            if self.table_exists(tbl.name):
                get_db().engine.execute(tbl.delete())
                tbl.drop(get_db().engine)

        get_db().get_session().expunge_all()
        get_db().get_session().expire_all()

def get_db():
    """
    :rtype: DB
    """
    if not DB.instance:
        DB.instance = DB()
    return DB.instance
