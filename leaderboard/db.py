import json
from os.path import expanduser, join, exists

from sqlalchemy import (
    create_engine
)

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


def conn_str():
    conn_tmpl = 'postgresql+pg8000://%(user)s:%(password)s@localhost/%(database)s'  # NOQA
    jdata = load_home_config()
    if not jdata:
        jdata = load_etc_config()
    return conn_tmpl % jdata


def _load_config(fpath):
    try:
        db_json = open(fpath)
        if exists(fpath):
            return json.load(db_json)
    except:
        return None


def load_etc_config():
    """
    Return the JSON blob from the /etc directory, or None if the
    file can't be loaded.
    """
    fpath = '/etc/mozilla/stumbler_leaderboard/db.json'
    return _load_config(fpath)


def load_home_config():
    """
    Return the JSON blob from the home directory, or None if the
    file can't be loaded.
    """
    fpath = join(expanduser("~"), ".stumbler_leaderboard", 'db.json')
    return _load_config(fpath)


def get_engine(uri):
    options = {
        'pool_recycle': 3600,
        'pool_size': 10,
        'pool_timeout': 10,
        'max_overflow': 10,
        'echo': False,
    }
    options['connect_args'] = {'charset': 'utf8'}
    options['execution_options'] = {'autocommit': True}
    return create_engine(uri, **options)


session_factory = scoped_session(sessionmaker(expire_on_commit=False,
                                              autocommit=True))

dsn = conn_str()
engine = get_engine(dsn)
Base = declarative_base(engine)


def init_sessions():
    # Setup the global database engine and session manager
    session_factory.configure(bind=engine)

    # TODO: this is terrible - fix this
    from leaderboard.models.db import get_db

    return get_db()
