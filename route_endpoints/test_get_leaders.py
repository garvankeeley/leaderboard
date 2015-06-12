from models.country_bounds import CountryBounds
from models.db import get_db
from models.user import User
from models.calendar import get_current_week_table_class
from route_endpoints import get_leaders
from submit_user_observations import add_stumbles_for_user
import test_submit

class TestLeaders(object):
    def setup(self):
        get_db().drop_all()
        get_db().create_all()

    def teardown(self):
        get_db().drop_all()

    def test_leaders(self):
        user = test_submit.create_one_user()
        test_submit.submit_helper(test_submit.submitted_json, user)

        json = '''
            [
                { "tile_easting_northing":"100,-700", "observations":200 },
                { "tile_easting_northing":"100,-700", "observations":3 }
            ]
        '''

        test_submit.submit_helper(json, user)
        result = get_leaders.get_leaders(29)
        assert result
        user_result, total = result[0]
        assert user_result == user
        assert total == 101
