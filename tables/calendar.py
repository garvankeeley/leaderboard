import datetime
import pg8000
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, and_
from sqlalchemy.orm import relationship, backref
from tile import Tile
from user import User
from db import get_db

def weekly_table_name():
    return "WEEK_%d_PER_TILE_PER_USER" % week_num_of_year()

def week_num_of_year():
    return datetime.datetime.now().isocalendar()[1]

def year_and_month_num():
    now = datetime.datetime.now()
    return "%d%d" % (now.year, now.month)

__week_classes = {}

def get_week_table_class(week_of_year):
    tablename = 'week%d' % week_of_year
    if tablename in __week_classes:
        return __week_classes[tablename]

    class CalenderReportPerUserAndTile(object):
        __tablename__ = tablename
        id = Column(Integer, primary_key=True)

        @declared_attr
        def user_id(cls):
            return Column(Integer, ForeignKey('user.id'))

        @declared_attr
        def tile_id(cls):
            return Column(Integer, ForeignKey('tile.id'))

        observation_count = Column(BigInteger)

    class Week(get_db().Base, CalenderReportPerUserAndTile):
        tile = relationship(Tile)
        user = relationship(User, backref=backref(tablename + 's'))

    #User.current_weeks = relationship(Week)
    __week_classes[tablename] = Week
    return Week


def get_week_table_stats(user, tile):
    Week = get_week_table_class(0)
    # session.query(User, Tile, Week)
    #user.current_weeks
    return get_db().session.query(Week).filter(and_(Week.user == user, Week.tile == tile)).first()

def insert_or_update_week(user, tile):
    Week = get_week_table_class(0)

    from sqlalchemy.engine.reflection import Inspector
    inspector = Inspector.from_engine(get_db().engine)
    if not Week.__tablename__ in inspector.get_table_names():
        get_db().metadata.create_all(get_db().engine)
        get_db().session.commit()

    existing = get_week_table_stats(user, tile)
    if existing:
        return existing

    w = Week()
    w.user = user
    w.tile = tile
    get_db().session.add(w)
    return w