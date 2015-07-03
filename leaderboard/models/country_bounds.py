from geoalchemy2 import Geometry, func
from sqlalchemy import Column, Integer, String
from leaderboard.geo_util import coord_sys as cs
from leaderboard.db import session_factory
from leaderboard.geo_util.coord_sys import WGS84_LATLON_CODE
from leaderboard.models.db import get_db

creation_command = 'ogr2ogr -f PostgreSQL PG:"port=5432" *.geo.json -nln country_bounds'

class CountryBounds(get_db().Base):
    __tablename__ = 'country_bounds'
    ogc_fid = Column(Integer, primary_key=True)
    wkb_geometry = Column(Geometry(geometry_type='Geometry', srid=cs.WGS84_LATLON_CODE))
    name = Column(String, nullable=False)

    @staticmethod
    def coord_sys():
        return cs.WGS84_LATLON_CODE

    @staticmethod
    def load_countries():
        import ogr
        import os
        pwd = os.path.dirname(os.path.abspath(__file__))
        infile = "%s/../fixtures/world.geo.json" % pwd
        drv = ogr.GetDriverByName('GeoJSON')
        assert drv
        ds = drv.Open(infile)
        layer = ds.GetLayer(0)
        srs = ogr.osr.SpatialReference()
        srs.ImportFromEPSG(WGS84_LATLON_CODE)
        session = session_factory()
        with session.begin(subtransactions=True):
            for feature in layer:
                id = feature.GetFID()
                name = feature.GetField(0)
                geo = feature.GetGeometryRef()
                wkb = 'SRID=%d;%s' % (CountryBounds.coord_sys(), geo.ExportToWkt())
                country = CountryBounds(ogc_fid=id, wkb_geometry=wkb, name=name)
                session.add(country)

    @staticmethod
    def set_country_for_tile(tile, use_intersect=False, use_nearby=False):
        from tile import Tile
        assert isinstance(tile, Tile)
        geo = tile.geo_as_wgs84()

        session = session_factory()
        with session.begin(subtransactions=True):
            result = session.query(CountryBounds).filter(
                CountryBounds.wkb_geometry.ST_Contains(func.ST_Centroid(geo)))
            c = result.first()

            if not c or use_intersect:
                result = session.query(CountryBounds).filter(\
                                CountryBounds.wkb_geometry.ST_Intersects(geo))
                c = result.first()

            if not c or use_nearby:
                # https://github.com/geoalchemy/geoalchemy2/issues/94 broken <->
                # also doesn't work SELECT ogc_fid FROM country_bounds ORDER BY wkb_geometry <-> ST_Centroid('%s') LIMIT 1
                nearby = '''
                    WITH index_query AS (
                      SELECT ST_Distance(wkb_geometry, '%s') as d, name, ogc_fid
                        FROM country_bounds
                      ORDER BY wkb_geometry <-> '%s' LIMIT 10)
                      SELECT ogc_fid
                        FROM index_query
                      ORDER BY d limit 1
                    ''' % (geo, geo)
                r = session.execute(nearby)
                c_id = r.fetchone()[0]
                c = session.query(CountryBounds).filter_by(ogc_fid=c_id).first()

            tile.country = c
