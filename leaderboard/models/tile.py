import math

from sqlalchemy import Column, BigInteger, Integer, ForeignKey, func
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, backref

from leaderboard.geo_util import coord_sys as cs
from leaderboard.models.db import get_db
from leaderboard.db import session_factory, Base
from leaderboard.models.country_bounds import CountryBounds
from leaderboard.geo_util import coord_utils


class Tile(Base):
    __tablename__ = 'tile'
    id = Column(BigInteger, primary_key=True)
    country_id = Column(Integer, ForeignKey('country_bounds.ogc_fid'))
    country = relationship(CountryBounds, backref=backref('tiles'))
    geometry = Column(Geometry(geometry_type='POLYGON', srid=cs.WEB_MERCATOR_CODE))

    @staticmethod
    def coord_sys():
        return cs.WEB_MERCATOR_CODE

    def geo_as_wgs84(self):
        session = session_factory()
        ewkt = "'" + session.execute(func.ST_AsEWKT(self.geometry)).first().values()[0] + "'" + '::geometry'
        #select ST_Transform('SRID=3785;POLYGON((-8839000 5419000,-8839000 5419500,-8838500 5419500,-8838500 5419000,-8839000 5419000))', 4326);
        r = session.execute("select ST_AsEWKT(ST_Transform(%s, %d))" % (ewkt, cs.WGS84_LATLON_CODE))
        return r.fetchone()[0]

    @staticmethod
    def get_tile_wgs84(lon, lat):
        easting, northing = coord_utils.db_get_easting_northing(lon, lat)
        return Tile.get_tile_mercator(easting, northing)

    @staticmethod
    def get_tile_mercator(easting, northing):
        session = session_factory()
        with session.begin(subtransactions=True):
            r = session.query(Tile).filter(func.ST_Contains(
                Tile.geometry, func.ST_SetSRID(func.ST_Point(easting, northing), cs.WEB_MERCATOR_CODE))).first()
            if r:
                return r

        ewkt = Tile.create_tile_ewkt_mercator(easting, northing)
        tile = Tile()
        tile.geometry = ewkt
        CountryBounds.set_country_for_tile(tile)
        return tile

    @staticmethod
    def create_tile_ewkt_wgs84(lon, lat):
        easting, northing = coord_utils.db_get_easting_northing(lon, lat)
        return Tile.create_tile_ewkt_mercator(easting, northing)

    @staticmethod
    def create_tile_ewkt_mercator(easting, northing):
        # point to mercator, find nearest grid tile lower left
        e_ll = math.floor(easting / 1000.0 * 2.0) / 2.0 * 1000.0
        n_ll = math.floor(northing / 1000.0 * 2.0) / 2.0 * 1000.0
        dist_m = 500
        geo = [(e_ll, n_ll), (e_ll, n_ll + dist_m), (e_ll + dist_m, n_ll + dist_m),
               (e_ll + dist_m, n_ll), (e_ll, n_ll)]
        geo_string = 'POLYGON((' + ','.join([' '.join([str(a) for a in x]) for x in geo]) + '))'
        return 'SRID=%d;%s' % (cs.WEB_MERCATOR_CODE, geo_string)
