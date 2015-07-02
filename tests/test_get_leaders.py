from leaderboard.route_endpoints.get_leaders import get_leaders_for_country

import test_submit

from test_base import BaseTest
from nose.tools import eq_


class TestLeaders(BaseTest):

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
        eq_(row0['name'], user.nickname)
        eq_(row0['observations'], str(101))

        user2 = test_submit.create_one_user()
        test_submit.submit_helper(test_submit.canada_observations_json, user2)
        test_submit.submit_helper(test_submit.canada_observations_json, user2)
        result = get_leaders_for_country(29)
        assert result
        row0 = result['leaders'][0]
        eq_(row0['name'], user2.nickname)
        eq_(row0['observations'], str(202))
