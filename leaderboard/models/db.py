from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.engine.reflection import Inspector
from leaderboard.db import engine, Base
from os.path import expanduser, join, exists

import json

from leaderboard.db import session_factory


class DB(object):
    instance = None

    def __init__(self):
        jdata = self.load_home_config()
        if not jdata:
            jdata = self.load_etc_config()

        if not jdata:
            raise RuntimeError("Can't load JSON configuration")

        self.engine = engine

        self.session_factory = scoped_session(sessionmaker(bind=self.engine,
                                              expire_on_commit=False,
                                              autocommit=True))

    def _load_config(self, fpath):
        try:
            db_json = open(fpath)
            if exists(fpath):
                return json.load(db_json)
        except:
            return None

    def load_etc_config(self):
        """
        Return the JSON blob from the /etc directory, or None if the
        file can't be loaded.
        """
        fpath = '/etc/mozilla/stumbler_leaderboard/db.json'
        return self._load_config(fpath)

    def load_home_config(self):
        """
        Return the JSON blob from the home directory, or None if the
        file can't be loaded.
        """
        fpath = join(expanduser("~"), ".stumbler_leaderboard", 'db.json')
        return self._load_config(fpath)

    def table_exists(self, name):
        inspector = Inspector.from_engine(get_db().engine)
        return name in inspector.get_table_names()

    def get_metadata(self):
        return Base.metadata

    def create_all(self):
        from leaderboard.models.country_bounds import CountryBounds  # NOQA
        from leaderboard.models.contributor import Contributor       # NOQA
        from leaderboard.models.tile import Tile    # NOQA
        do_load = not self.table_exists(CountryBounds.__tablename__)
        self.get_metadata().create_all(self.engine)

        if do_load:
            CountryBounds.load_countries()

    def drop_all(self):
        from leaderboard.models.country_bounds import CountryBounds  # NOQA
        from leaderboard.models.contributor import Contributor  # NOQA
        from leaderboard.models.tile import Tile   # NOQA
        from leaderboard.models.calendar_report_factory import get_current_quartermonth_table_class
        wk = get_current_quartermonth_table_class()
        if self.table_exists(wk.__tablename__):
            t = wk.__table__
            t.drop(get_db().engine)
        for tbl in reversed(get_db().get_metadata().sorted_tables):
            if self.table_exists(tbl.name):
                get_db().engine.execute(tbl.delete())
                tbl.drop(get_db().engine)

        session = session_factory()
        with session.begin(subtransactions=True):
            session.expunge_all()
            session.expire_all()


def get_db():
    """
    :rtype: DB
    """
    if not DB.instance:
        DB.instance = DB()
    return DB.instance
