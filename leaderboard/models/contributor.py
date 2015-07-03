from sqlalchemy import Column, Integer, String
from db import get_db

class Contributor(get_db().Base):
    __tablename__ = 'contributor'
    id = Column(Integer, primary_key=True)
    # nickname should be unique?
    nickname = Column(String, nullable=False)
    email = Column(String)
    bearer_token = Column(String)

    def get_reports_weekly(self):
        from leaderboard.models.calendar_report_factory import get_current_quartermonth_table_class
        weeks = getattr(self, '%ss' % get_current_quartermonth_table_class().__tablename__)
        return weeks
