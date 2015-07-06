from leaderboard.db import session_factory
from leaderboard.models.tile import Tile
from leaderboard.models.contributor import Contributor
from leaderboard.models.reportweeks import insert_or_update_reportweek
key_tile_easting_northing = 'tile_easting_northing'
key_observations = 'observations'


def add_stumbles_for_contributor(email, display_name, query_json):
    # Hack
    json_object = query_json

    session = session_factory()
    with session.begin(subtransactions=True):
        contributor = session.query(Contributor).filter_by(email=email).first()

        if contributor is None:
            contributor = Contributor(nickname=display_name,
                                      email=email)
            session.add(contributor)
        elif contributor.nickname != display_name:
            # Update the displayname
            contributor.nickname = display_name

            # Need to add to the session to mark as dirty
            session.add(contributor)

        for row in json_object['items']:
            tile_coord = row[key_tile_easting_northing]
            east, north = tile_coord.split(",")
            tile = Tile.get_tile_mercator(int(float(east)), int(float(north)))
            week_per_tile = insert_or_update_reportweek(contributor, tile)
            obs = row[key_observations]
            if not week_per_tile.observation_count:
                week_per_tile.observation_count = 0
            week_per_tile.observation_count += obs

    return True
