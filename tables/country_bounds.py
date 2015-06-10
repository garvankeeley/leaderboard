from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String
from ..geo_util import coord_sys as cs
import db

creation_command = 'ogr2ogr -f PostgreSQL PG:"port=5432" *.geo.json -nln country_bounds'

class CountryBounds(db.get_db().Base):
    __tablename__ = 'country_bounds'
    ogc_fid = Column(Integer, primary_key=True)
    wkb_geometry = Column(Geometry(geometry_type='Geometry', srid=cs.WGS84_LATLON_CODE))
    name = Column(String, nullable=False)

    @staticmethod
    def coord_sys():
        return cs.WGS84_LATLON_CODE
