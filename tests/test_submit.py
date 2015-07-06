from leaderboard.db import session_factory
from leaderboard.models.contributor import Contributor
from leaderboard.models.reportweeks import get_current_reportweek_class
from leaderboard.route_endpoints.submit_contributor_observations import add_stumbles_for_contributor
from test_base import BaseTest
from nose.tools import eq_

canada_observations_json = '''
    [
        { "tile_easting_northing":"-8872100,5435700", "observations":100 },
        { "tile_easting_northing":"-8872100,5435700", "observations":1 }
    ]
'''

BEARER_TOKEN = 'abc'


class TestSubmit(BaseTest):
    def test_submit(self):
        contributor = create_one_contributor()
        submit_helper(canada_observations_json, contributor)
        # check contributor has 1 tile, 1 weekX row, and total obs is 101
        weekly_per_tile = contributor.get_reports_weekly()
        eq_(len(weekly_per_tile), 1)
        single_week = weekly_per_tile[0]
        assert isinstance(single_week, get_current_reportweek_class())
        eq_(single_week.observation_count, 101)
        eq_(single_week.tile.country.name.lower(), 'canada')

    def test_submit_server_new_nick(self):
        import time

        session = session_factory()
        contributor = create_one_contributor()
        with session.begin():
            session.add(contributor)
            nick = contributor.nickname
        nickname = time.time()
        add_stumbles_for_contributor(contributor.email, nickname,
                                     canada_observations_json)
        # check contributor has 1 tile, 1 weekX row, and total obs is 101
        weekly_per_tile = contributor.get_reports_weekly()
        eq_(len(weekly_per_tile), 1)
        single_week = weekly_per_tile[0]
        assert isinstance(single_week, get_current_reportweek_class())
        eq_(single_week.observation_count, 101)
        eq_(single_week.tile.country.name.lower(), 'canada')

        # Verify that the contributor nickname was updated
        eq_(contributor.nickname, nickname)


contributor_counter = 0


def create_one_contributor():
    global contributor_counter
    contributor_counter += 1
    contributor = Contributor()
    contributor.email = 'foo@foo.com%d' % contributor_counter
    contributor.nickname = 'nick%d' % contributor_counter
    session = session_factory()
    with session.begin(subtransactions=True):
        session.add(contributor)
    return contributor


def submit_helper(json, contributor):
    add_stumbles_for_contributor(contributor.email, contributor.nickname, json)
