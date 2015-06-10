import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, and_
from sqlalchemy.orm import relationship, backref
from tables.tile import Tile
from tables.user import User

Base = declarative_base()

def weekly_table_name():
    return "WEEK_%d_PER_TILE_PER_USER" % week_num_of_year()

def week_num_of_year():
    return datetime.datetime.now().isocalendar()[1]

def year_and_month_num():
    now = datetime.datetime.now()
    return "%d%d" % (now.year, now.month)

def get_week_table(week_of_year):
    tablename = 'week%d' % week_of_year

    class CalenderReportPerUserAndTile():
        __tablename__ = tablename
        id = Column(Integer, primary_key=True)

        user_id = Column(Integer, ForeignKey('user.id'))
        user = relationship('user', backref=backref(tablename + 's'))

        tile_id = Column(BigInteger, ForeignKey('tile.id'))
        tile = relationship(Tile)

        observation_count = Column(BigInteger)

    class Week(Base, CalenderReportPerUserAndTile):
        pass

    #User.current_weeks = relationship(Week)

    return Week


def get_week_table_stats(user, tile):
    Week = get_week_table(0)
    # session.query(User, Tile, Week)
    #user.current_weeks
    Week.filter(and_(Week.user == user, Week.tile == tile))

