from sqlalchemy import (
    create_engine
)

from sqlalchemy.orm import sessionmaker, scoped_session


def conn_str():
    conn_tmpl = 'postgresql+pg8000://%(user)s:%(password)s@localhost/%(database)s'
    jdata = {"user": "mozstumbler",
             "password": "stumbler",
             "database": "leaderboard"}
    return conn_tmpl % jdata


def get_engine(uri):
    options = {
        'pool_recycle': 3600,
        'pool_size': 10,
        'pool_timeout': 10,
        'max_overflow': 10,
        'echo': False,
    }
    options['connect_args'] = {'charset': 'utf8'}
    options['execution_options'] = {'autocommit': False}
    return create_engine(uri, **options)

session_factory = scoped_session(sessionmaker(expire_on_commit=False,
                                      autocommit=True))



def init_sessions():
    # Setup the global database engine and session manager
    engine = get_engine(conn_str())
    session_factory.configure(bind=engine)

    # TODO: this is terrible - fix this
    from leaderboard.models.db import get_db

    return get_db()
