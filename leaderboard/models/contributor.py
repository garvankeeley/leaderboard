from sqlalchemy import Column, Integer, String
from leaderboard.db import Base


class Contributor(Base):
    __tablename__ = 'contributor'
    id = Column(Integer, primary_key=True)
    # nickname should be unique?
    nickname = Column(String, nullable=False)
    email = Column(String)

    def get_reports_weekly(self):
        from leaderboard.models.reportweeks import get_current_reportweek_class

        weeks = getattr(self, '%ss' % get_current_reportweek_class().__tablename__)
        return weeks
