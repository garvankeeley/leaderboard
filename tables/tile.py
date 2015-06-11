from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, Integer, ForeignKey, func
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, backref
from ..geo_util import coord_sys as cs
from db import get_db
from country_bounds import CountryBounds


class Tile(get_db().Base):
    __tablename__ = 'tile'
    id = Column(BigInteger, primary_key=True)
    country_id = Column(Integer, ForeignKey('country_bounds.ogc_fid'))
    country = relationship(CountryBounds, backref=backref('tiles'))
    geometry = Column(Geometry(geometry_type='POLYGON', srid=cs.WEB_MERCATOR_CODE))

    @staticmethod
    def coord_sys():
        return cs.WEB_MERCATOR_CODE

    def geo_as_wgs84(self):
        ewkt = "'" + get_db().engine.execute(func.ST_AsEWKT(self.geometry)).first().values()[0] + "'" + '::geometry'
        #select ST_Transform('SRID=3785;POLYGON((-8839000 5419000,-8839000 5419500,-8838500 5419500,-8838500 5419000,-8839000 5419000))', 4326);
        r = get_db().engine.execute("select ST_AsEWKT(ST_Transform(%s, %d))" % (ewkt, cs.WGS84_LATLON_CODE))
        return r.fetchone()[0]
