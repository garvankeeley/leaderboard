import json
from leaderboard.db import session_factory
from leaderboard.models.tile import Tile
from leaderboard.models.contributor import Contributor
from leaderboard.models.calendar_factory import insert_or_update_week
key_tile_easting_northing = 'tile_easting_northing'
key_observations = 'observations'


def add_stumbles_for_user(email, display_name, login_token, query_json):
    session = session_factory()
    with session.begin(subtransactions=True):
        user = session.query(Contributor).filter_by(email=email).first()
        if user.nickname != display_name:
            user.nickname = display_name
            session.add(user)

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

    return True
