import json
from models.db import get_db
from models.tile import Tile
from models.user import User
from models.calendar_factory import insert_or_update_week
key_tile_easting_northing = 'tile_easting_northing'
key_observations = 'observations'


def add_stumbles_for_user(email, login_token, query_json):
    user = get_db().session.query(User).filter_by(email=email).first()
    if not user:
        return False

    if not user.bearer_token or user.bearer_token != login_token:
        return False

    json_object = json.loads(query_json)
    for row in json_object:
        tile_coord = row[key_tile_easting_northing]
        east, north = tile_coord.split(",")
        tile = Tile.get_tile_mercator(int(east), int(north))
        week_per_tile = insert_or_update_week(user, tile)
        obs = row[key_observations]
        if not week_per_tile.observation_count:
            week_per_tile.observation_count = 0
        week_per_tile.observation_count += obs

    get_db().commit()

    return True