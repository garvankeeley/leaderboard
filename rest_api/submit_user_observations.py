from models.db import get_db
from models.tile import Tile
from models.user import User

key_tile_easting_northing = 'tile_easting_northing'
key_cellcount = 'cellcount'
key_wificount = 'wificount'

def add_stumbles_for_user(email, login_token, query_json):
    tile_coord = query_json[key_tile_easting_northing]
    cellcount = query_json[key_cellcount]
    wificount = query_json[key_wificount]

    user = get_db().session.query(User).filter_by(email=email).first()
    if not user:
        return

    if not user.bearer_token or user.bearer_token != login_token:
        return

    tile = Tile.get_tile_mercator(*tile_coord.split(","))

    #for this user and tile, update the weekly report

