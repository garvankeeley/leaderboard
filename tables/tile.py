from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, Integer, ForeignKey
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, backref
from geo_util import coord_sys as cs

Base = declarative_base()

class Tile(Base):
    __tablename__ = 'tile'
    id = Column(BigInteger, primary_key=True)
    country_id = Column(Integer, ForeignKey('country_bounds.id'))
    country = relationship('country_bounds', backref=backref('tiles'))
    geometry = Column(Geometry(geometry_type='POLYGON', srid=cs.WEB_MERCATOR_CODE))

    @staticmethod
    def coord_sys():
        return cs.WEB_MERCATOR_CODE

