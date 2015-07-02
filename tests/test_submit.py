from leaderboard.db import session_factory
from leaderboard.models.user import User
from leaderboard.models.calendar_factory import get_current_week_table_class
from leaderboard.route_endpoints.submit_user_observations import add_stumbles_for_user
from test_base import BaseTest
from nose.tools import eq_

canada_observations_json = '''
    [
        { "tile_easting_northing":"-8872100,5435700", "observations":100 },
        { "tile_easting_northing":"-8872100,5435700", "observations":1 }
    ]
'''


class TestSubmit(BaseTest):
    def test_submit(self):
        user = create_one_user()
        submit_helper(canada_observations_json, user)
        # check user has 1 tile, 1 weekX row, and total obs is 101
        weekly_per_tile = user.get_reports_weekly()
        eq_(len(weekly_per_tile), 1)
        single_week = weekly_per_tile[0]
        assert isinstance(single_week, get_current_week_table_class())
        eq_(single_week.observation_count, 101)
        eq_(single_week.tile.country.name.lower(), 'canada')

    def test_submit_server_new_nick(self):
        import time
        session = session_factory()
        user = create_one_user()
        with session.begin():
            session.add(user)
            nick = user.nickname
        nickname = time.time()
        add_stumbles_for_user(user.email, nickname, user.bearer_token, canada_observations_json)
        # check user has 1 tile, 1 weekX row, and total obs is 101
        weekly_per_tile = user.get_reports_weekly()
        eq_(len(weekly_per_tile), 1)
        single_week = weekly_per_tile[0]
        assert isinstance(single_week, get_current_week_table_class())
        eq_(single_week.observation_count, 101)
        eq_(single_week.tile.country.name.lower(), 'canada')

        # Verify that the user nickname was updated
        eq_(user.nickname, nickname)


    def test_bad_token(self):
        user = User()
        user.email = 'a@b.com'
        user.nickname = 'a'

        with self.session.begin():
            self.session.add(user)

        args = user.email, user.nickname, user.bearer_token, ""
        ok = add_stumbles_for_user(*args)
        assert not ok
        user.bearer_token = 'abc'
        args = user.email, user.nickname, 'cdf', ""
        ok = add_stumbles_for_user(*args)
        assert not ok

user_counter = 0


def create_one_user():
    global user_counter
    user_counter += 1
    user = User()
    user.bearer_token = 'abc%d' % user_counter
    user.email = 'foo@foo.com%d' % user_counter
    user.nickname = 'nick%d' % user_counter
    session = session_factory()
    with session.begin(subtransactions=True):
        session.add(user)
    return user


def submit_helper(json, user):
    add_stumbles_for_user(user.email, user.nickname, user.bearer_token, json)
