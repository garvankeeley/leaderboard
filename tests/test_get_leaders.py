from leaderboard.models.db import get_db
from leaderboard.route_endpoints import get_leaders
from leaderboard.route_endpoints.get_leaders import get_leaders_for_country

import test_submit


class TestLeaders(object):
    def setup(self):
        get_db().drop_all()
        get_db().create_all()

    def teardown(self):
        get_db().drop_all()

    def test_leaders(self):
        user = test_submit.create_one_user()
        test_submit.submit_helper(test_submit.canada_observations_json, user)

        json = '''
            [
                { "tile_easting_northing":"100,-700", "observations":200 },
                { "tile_easting_northing":"100,-700", "observations":3 }
            ]
        '''

        test_submit.submit_helper(json, user)
        result = get_leaders_for_country(29)
        assert result
        row0 = result['leaders'][0]
        assert row0['name'] == user.nickname
        assert row0['observations'] == 101

        user2 = test_submit.create_one_user()
        test_submit.submit_helper(test_submit.canada_observations_json, user2)
        test_submit.submit_helper(test_submit.canada_observations_json, user2)
        result = get_leaders.get_leaders(29)
        assert result
        row0 = result['leaders'][0]
        assert row0['name'] == user2.nickname
        assert row0['observations'] == 202
