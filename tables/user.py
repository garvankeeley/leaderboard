from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, Integer, String
from db import get_db


class User(get_db().Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    # nickname should be unique?
    nickname = Column(String, nullable=False)
    email = Column(String)
    bearer_token = Column(String)
    total_observations = Column(BigInteger)

