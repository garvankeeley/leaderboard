from db import get_db

class Test(object):
    def setup(self):
        print 'setup'

    def teardown(self):
        for tbl in reversed(get_db().metadata.sorted_tables):
            get_db().engine.execute(tbl.delete())

    def test1(self):
        print 'test1'
        from user import User
        from tile import Tile
        import calendar
        from country_bounds import CountryBounds
        db = get_db()
        db.metadata.create_all(db.engine)
        db.session.commit()

        user = User()
        user.nickname = 'nick'

        tile = Tile()

        db.session.add(user)
        db.session.add(tile)
        db.session.commit()

        w = calendar.insert_or_update_week(user, tile)
        db.session.commit()
        assert True

