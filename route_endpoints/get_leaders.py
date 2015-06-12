from models import calendar, db, user, tile


def get_leaders(country_id):
    Week = calendar.get_current_week_table_class()
    q = db.get_db().get_session().query(Week, user.User, tile.Tile).\
        filter(tile.Tile.country_id == country_id).\
        filter(Week.user_id == user.User.id).\
        filter(Week.tile_id == tile.Tile.id)
    result = q.all()
    if result:
        assert isinstance(result[0][0], Week)
        assert isinstance(result[0][1], user.User)
        assert isinstance(result[0][2], tile.Tile)
    return result
