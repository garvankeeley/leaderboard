from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)

from sqlalchemy.ext.declarative import declarative_base 
Base = declarative_base()
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, backref

class Foo(Base):
    __tablename__ = 'foo'
    id = Column(Integer, primary_key=True)
    name = Column(String, default='gi')

class Doo(Base):
    __tablename__ = 'doo'
    id = Column(Integer, primary_key=True)
    foo_id = Column(Integer, ForeignKey('foo.id'))

Doo.foo = relationship('Foo', backref=backref('doos'))


