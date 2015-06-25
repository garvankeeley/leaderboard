from leaderboard.db import init_sessions, session_factory


class BaseTest(object):
    """
    This baseclass should be use for testcases to ensure that tables
    are all setup and a session is ready for use.

    The database is reset by rolling back transactions in the
    teardown.

    Any subclasses that override the teardown must call
    BaseTest.teardown.
    """
    def setup(self):
        if not hasattr(self, 'db'):
            self.db = init_sessions()
            self.db.drop_all()
            self.db.create_all()
        self.session = session_factory()

    def teardown(self):
        self.session.rollback()
