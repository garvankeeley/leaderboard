import calendar
import datetime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, ForeignKey, BigInteger, and_
from sqlalchemy.orm import relationship, backref
from tile import Tile
from contributor import Contributor
from db import get_db
from leaderboard.db import session_factory


def quartermonth_name_by_year_and_quarter_month():
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

__quartermonth_classes = {}

def get_quartermonth_table_class(quartermonth_name=None):
    if not quartermonth_name:
        quartermonth_name = quartermonth_name_by_year_and_quarter_month()

    tablename = 'quartermonth%s' % quartermonth_name
    if tablename in __quartermonth_classes:
        return __quartermonth_classes[tablename]

    class CalenderReportPerContributorAndTile(object):
        __tablename__ = tablename
        id = Column(Integer, primary_key=True)

        @declared_attr
        def contributor_id(cls):
            return Column(Integer, ForeignKey(Contributor.id))

        @declared_attr
        def tile_id(cls):
            return Column(Integer, ForeignKey(Tile.id))

        observation_count = Column(BigInteger)

    class QuarterMonth(get_db().Base, CalenderReportPerContributorAndTile):
        tile = relationship(Tile)
        contributor = relationship(Contributor, backref=backref(tablename + 's'))

    __quartermonth_classes[tablename] = QuarterMonth
    return QuarterMonth


def get_current_quartermonth_table_class():
    quartermonth_class = get_quartermonth_table_class(None)
    return quartermonth_class

def get_quartermonth_table_for_contributor_and_tile(contributor, tile):
    QuarterMonth = get_current_quartermonth_table_class()
    session = session_factory()
    with session.begin(subtransactions=True):
        return session.query(QuarterMonth).filter(and_(QuarterMonth.contributor == contributor, QuarterMonth.tile == tile)).first()



def insert_or_update_quartermonth(contributor, tile):
    """
    This is ugly.  We should change this to use statically generated
    tables.  The table creation should be avoided at runtime to just a
    few discrete events so that we have a predictable schema.
    """
    QuarterMonth = get_current_quartermonth_table_class()

    db = get_db()
    session = session_factory()
    with session.begin(subtransactions=True):
        if not db.table_exists(QuarterMonth.__tablename__):
            db.get_metadata().create_all(db.engine)

        existing = get_quartermonth_table_for_contributor_and_tile(contributor, tile)
        if existing:
            return existing

        w = QuarterMonth()
        w.contributor = contributor
        w.tile = tile
        session.add(w)
        return w
