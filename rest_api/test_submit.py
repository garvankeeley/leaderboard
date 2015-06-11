from models.country_bounds import CountryBounds
from models.db import get_db
from models.user import User

submitted_json = '''
[
{ "tile_northing_easting":"-8872100,5435700", "cellcount":"100","wificount":"50 },
{ "tile_northing_easting":"-8872100,5435700", "cellcount":"100","wificount":"50 },
]
'''

class TestSubmit(object):
    def setup(self):
        print 'setup'
        self.teardown()
        db = get_db()
        db.metadata.create_all(db.engine)
        db.session.commit()

        CountryBounds.load_countries()

    def teardown(self):
        for tbl in reversed(get_db().metadata.sorted_tables):
            get_db().engine.execute(tbl.delete())

    def test(self):
        user = User()
