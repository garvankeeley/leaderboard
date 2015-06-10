from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import geo_util.coord_sys as cs

Base = declarative_base()

creation_command = 'ogr2ogr -f PostgreSQL PG:"port=5432" *.geo.json -nln country_bounds'

class CountryBounds(Base):
    __tablename__ = 'country_bounds'
    ogc_fid = Column(Integer, primary_key=True)
    wkb_geometry = Column(Geometry(geometry_type='POLYGON', srid=cs.WGS84_LATLON_CODE))
    name = Column(String, nullable=False)

    @staticmethod
    def coord_sys():
        return cs.WGS84_LATLON_CODE
