from models.country_bounds import CountryBounds
from models.db import get_db
from models.user import User
from models.calendar import get_current_week_table_class
from submit_user_observations import add_stumbles_for_user

submitted_json = '''
    [
        { "tile_easting_northing":"-8872100,5435700", "observations":100 },
        { "tile_easting_northing":"-8872100,5435700", "observations":1 }
    ]
'''

class TestSubmit(object):
    def setup(self):
        get_db().drop_all()
        get_db().create_all()

    def teardown(self):
        get_db().drop_all()

    def test_submit(self):
        user = User()
        user.bearer_token = 'abc'
        user.email = 'foo@foo.com'
        user.nickname = 'nick'
        get_db().add(user)
        get_db().commit()
        add_stumbles_for_user(user.email, user.bearer_token, submitted_json)
        # check user has 1 tile, 1 weekX row, and total obs is 101
        weekly_per_tile = user.get_reports_weekly()
        assert len(weekly_per_tile) == 1
        single_week = weekly_per_tile[0]
        assert isinstance(single_week, get_current_week_table_class())
        assert single_week.observation_count == 101
        assert single_week.tile.country.name.lower() == 'canada'

    def test_bad_token(self):
        user = User()
        user.email = 'a@b.com'
        user.nickname = 'a'
        get_db().add(user)
        get_db().commit()
        ok = add_stumbles_for_user(user.email, user.bearer_token, "")
        assert not ok
        user.bearer_token = 'abc'
        ok = add_stumbles_for_user(user.email, 'cdf', "")
        assert not ok
        get_db().commit()
