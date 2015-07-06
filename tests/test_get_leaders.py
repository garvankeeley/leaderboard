from leaderboard.route_endpoints.get_leaders import get_leaders_for_country

import test_submit
import json
from test_base import BaseTest
from nose.tools import eq_

class TestLeaders(BaseTest):

    def test_leaders(self):
        contributor = test_submit.create_one_contributor()
        canada_obs = test_submit.canada_observations_json
        test_submit.submit_helper(canada_obs, contributor)
        not_canada_obs = '''
            {"items":[
                { "tile_easting_northing":"100,-700", "observations":200 },
                { "tile_easting_northing":"100,-700", "observations":3 }
            ]}
        '''

        test_submit.submit_helper(not_canada_obs, contributor)
        result = get_leaders_for_country(29)
        assert result
        row0 = result['leaders'][0]
        eq_(row0['name'], contributor.nickname)
        eq_(row0['observations'], str(101))

        contributor2 = test_submit.create_one_contributor()
        test_submit.submit_helper(canada_obs, contributor2)
        test_submit.submit_helper(canada_obs, contributor2)
        result = get_leaders_for_country(29)
        assert result
        row0 = result['leaders'][0]
        eq_(row0['name'], contributor2.nickname)
        eq_(row0['observations'], str(202))
