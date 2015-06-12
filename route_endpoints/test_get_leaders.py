from models.country_bounds import CountryBounds
from models.db import get_db
from models.user import User
from models.calendar import get_current_week_table_class
from route_endpoints import get_leaders
from submit_user_observations import add_stumbles_for_user
import test_submit

class TestLeaders(object):
    def setup(self):
        print 'setup'
        get_db().drop_all()
        get_db().create_all()

    def teardown(self):
        get_db().drop_all()

    def test_leaders(self):
        t = test_submit.TestSubmit()
        t.test_submit()
        get_leaders.get_leaders(29)
        get_db().commit()
        assert True