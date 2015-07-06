import datetime
from sqlalchemy import Column, BigInteger, Integer, ForeignKey, and_
from leaderboard.models.contributor import Contributor
from leaderboard.db import session_factory, Base
from leaderboard.models.db import get_db
from leaderboard.models.tile import Tile


# Weeks are 1-53, every 5.6 years, a year has 53 weeks

def current_week_number():
    # clarify that number starts at zero
    assert(datetime.date(2015, 1, 1).isocalendar()[1] == 1)
    return datetime.datetime.now().isocalendar()[1]


_week_classes_cache = {}
def get_reportweek_class(week_num):
    assert(0 < week_num < 54)

    tablename = 'reportweek%d' % week_num
    if tablename in _week_classes_cache:
        return _week_classes_cache[tablename]

    class Week(Base):
        __table_classname__ = tablename
        id = Column(Integer, primary_key=True)
        contributor_id = Column(Integer, ForeignKey(Contributor.id))
        tile_id = Column(Integer, ForeignKey(Tile.id))
        observation_count = Column(BigInteger)

    _week_classes_cache[tablename] = Week
    return Week


def get_reportweek_for_contributor_and_tile(contributor, tile):
    week_class = get_reportweek_class(current_week_number())
    session = session_factory()
    with session.begin(subtransactions=True):
        return session.query(week_class).filter(and_(week_class.contributor_id == contributor,
                                                     week_class.tile_id == tile)).first()


def get_current_reportweek_class():
    return get_reportweek_class(current_week_number())


def insert_or_update_reportweek(contributor, tile):
    week_class = get_current_reportweek_class()
    db = get_db()
    session = session_factory()
    with session.begin(subtransactions=True):
        if not db.table_exists(week_class.__tablename__):
            db.get_metadata().create_all(db.engine)

        existing = get_reportweek_for_contributor_and_tile(contributor, tile)
        if existing:
            return existing

        w = week_class()
        w.contributor_id = contributor
        w.tile_id = tile
        session.add(w)
        return w
