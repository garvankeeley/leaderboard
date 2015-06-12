import math
from db import get_db
from country_bounds import CountryBounds
from geo_util import coord_utils
from user import User
from tile import Tile
import calendar

class Test(object):
    def setup(self):
        get_db().drop_all()
        get_db().create_all()

    def teardown(self):
        get_db().drop_all()

    def test_countries_id_is_correct(self):
        row = get_db().session.query(CountryBounds).filter_by(name='Afghanistan')
        assert row
        item = row.first()
        assert item.ogc_fid == 1

    def get_canada(self):
        item = get_db().session.query(CountryBounds).filter_by(name='Canada').first()
        assert isinstance(item, CountryBounds)
        return item

    def test_add_user_tile_and_report(self):
        print 'test1'
        db = get_db()

        user = User()
        user.nickname = 'nick'

        tile = Tile()

        db.session.add(user)
        db.session.add(tile)
        db.session.commit()

        w = calendar.insert_or_update_week(user, tile)
        db.session.commit()
        assert True

    def test_add_tile_for_coord(self):
        tile = Tile()
        mercator_coords = Tile.create_tile_ewkt_wgs84(-79.4, 43.7)
        tile.geometry = mercator_coords
        get_db().session.add(tile)
        get_db().session.commit()

        CountryBounds.set_country_for_tile(tile)
        canada = self.get_canada()
        assert tile.country == canada

        CountryBounds.set_country_for_tile(tile, use_intersect=True)
        assert tile.country == canada

        CountryBounds.set_country_for_tile(tile, use_nearby=True)
        assert tile.country == canada

    def test_coord_conversion(self):
        e1 = coord_utils.lon2x_m(-80)
        n1 = coord_utils.lat2y_m(44)
        e2, n2 = coord_utils.db_get_easting_northing(-80, 44)
        assert math.fabs(e1 - e2) < 5
        assert math.fabs(n1 - n2) < 5
