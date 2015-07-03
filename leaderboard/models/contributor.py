from sqlalchemy import Column, BigInteger, Integer, String
from db import get_db

class Contributor(get_db().Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    # nickname should be unique?
    nickname = Column(String, nullable=False)
    email = Column(String)
    bearer_token = Column(String)

    def get_reports_weekly(self):
        from leaderboard.models.calendar_factory import get_current_week_table_class
        weeks = getattr(self, '%ss' % get_current_week_table_class().__tablename__)
        return weeks
