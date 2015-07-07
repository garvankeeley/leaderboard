import math
from sqlalchemy.orm.exc import NoResultFound
from leaderboard.db import session_factory

from leaderboard.models.country_bounds import CountryBounds
from leaderboard.geo_util import coord_utils
from leaderboard.models.contributor import Contributor
from leaderboard.models.db import LeaderboardGlobals
from leaderboard.models.tile import Tile
from leaderboard.models import reportweeks
from test_base import BaseTest


class TestModels(BaseTest):
    def test_countries_id_is_correct(self):
        with self.session.begin(subtransactions=True):
            row = self.session.query(CountryBounds).filter_by(name='Afghanistan')
            assert row
            item = row.first()
            assert item.ogc_fid == 1

    def get_canada(self):
        with self.session.begin(subtransactions=True):
            item = self.session.query(CountryBounds).filter_by(name='Canada').first()
            assert isinstance(item, CountryBounds)
            return item

    def test_add_contributor_tile_and_report(self):
        with self.session.begin(subtransactions=True):
            contributor = Contributor()
            contributor.nickname = 'nick'

            tile = Tile()

            self.session.add(contributor)
            self.session.add(tile)

            reportweeks.insert_or_update_reportweek(contributor, tile)

    def test_add_tile_for_coord(self):
        with self.session.begin(subtransactions=True):
            tile = Tile()
            mercator_coords = Tile.create_tile_ewkt_wgs84(-79.4, 43.7)
            tile.geometry = mercator_coords
            self.session.add(tile)

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

    def test_weekly_rollover(self):
        # add data
        self.test_add_contributor_tile_and_report()
        week_class = reportweeks.get_current_reportweek_class()
        session = session_factory()
        rows = None
        try:
            rows = session.query(week_class).one()
        except NoResultFound:
            pass
        assert rows

        g = LeaderboardGlobals.get_globals()
        g.current_week = reportweeks.current_week_number() - 1

        # verify data gets truncated on next access
        week_class = reportweeks.get_current_reportweek_class()
        session = session_factory()
        rows = None
        try:
            rows = session.query(week_class).one()
        except NoResultFound:
            pass
        assert not rows
