import json
from leaderboard.db import session_factory
from leaderboard.models.tile import Tile
from leaderboard.models.contributor import Contributor
from leaderboard.models.calendar_report_factory import insert_or_update_quartermonth
key_tile_easting_northing = 'tile_easting_northing'
key_observations = 'observations'


def add_stumbles_for_contributor(email, display_name, login_token, query_json):
    session = session_factory()
    with session.begin(subtransactions=True):
        contributor = session.query(Contributor).filter_by(email=email).first()
        if contributor.nickname != display_name:
            contributor.nickname = display_name
            session.add(contributor)

        if not contributor:
            return False

        if not contributor.bearer_token or contributor.bearer_token != login_token:
            return False

        json_object = json.loads(query_json)
        for row in json_object:
            tile_coord = row[key_tile_easting_northing]
            east, north = tile_coord.split(",")
            tile = Tile.get_tile_mercator(int(east), int(north))
            week_per_tile = insert_or_update_quartermonth(contributor, tile)
            obs = row[key_observations]
            if not week_per_tile.observation_count:
                week_per_tile.observation_count = 0
            week_per_tile.observation_count += obs

    return True
