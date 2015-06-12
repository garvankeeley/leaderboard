from decimal import Decimal
from models import calendar, db, user, tile
from geoalchemy2 import func

def get_leaders(country_id):
    Week = calendar.get_current_week_table_class()
    q = db.get_db().get_session().query(user.User,
                                        func.sum(Week.observation_count).label('obs_sum')).\
        filter(tile.Tile.country_id == country_id).\
        filter(Week.user_id == user.User.id).\
        filter(Week.tile_id == tile.Tile.id).group_by(user.User.id)
    result = q.all()
    if result:
        assert isinstance(result[0][0], user.User)
        assert isinstance(result[0][1], Decimal)

    return result
