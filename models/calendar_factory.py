import calendar
import datetime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, ForeignKey, BigInteger, and_
from sqlalchemy.orm import relationship, backref
from tile import Tile
from user import User
from db import get_db


def week_name_by_year_and_quarter_month():
    now = datetime.datetime.now()
    days_of_month = calendar.monthrange(now.year, now.month)[1]

    if days_of_month < 29:
        month_quarter = (now.day - 1) // 7
    elif days_of_month > 30:
        month_quarter = (now.day - 1) // 8 if now.day < 25 else 3
    else:
        month_quarter = (now.day - 1) // 8 if now.day < 17 else (now.day - 17) // 7 + 2

    # divide month into quarters 1,2,3,4
    month_quarter += 1

    return "%d_%d_%d" % (now.year, now.month, month_quarter)

# def year_and_month_num():
#     now = datetime.datetime.now()
#     return "%d%d" % (now.year, now.month)

__week_classes = {}

def get_week_table_class(week_name=None):
    if not week_name:
        week_name == week_name_by_year_and_quarter_month()

    tablename = 'week%s' % week_name
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

    __week_classes[tablename] = Week
    return Week


def get_current_week_table_class():
    week_class = get_week_table_class(None)
    return week_class

def get_week_table_stats(user, tile):
    Week = get_current_week_table_class()
    return get_db().session.query(Week).filter(and_(Week.user == user, Week.tile == tile)).first()


def insert_or_update_week(user, tile):
    Week = get_current_week_table_class()

    db = get_db()
    if not db.table_exists(Week.__tablename__):
        db.get_metadata().create_all(get_db().engine)
        db.session.commit()

    existing = get_week_table_stats(user, tile)
    if existing:
        return existing

    w = Week()
    w.user = user
    w.tile = tile
    db.get_session().add(w)
    return w