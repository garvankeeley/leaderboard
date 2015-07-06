from sqlalchemy import Column, Integer, String
from leaderboard.db import Base, session_factory


class Contributor(Base):
    __tablename__ = 'contributor'
    id = Column(Integer, primary_key=True)
    # nickname should be unique?
    nickname = Column(String, nullable=False)
    email = Column(String)

    def get_report_counts_for_weeks(self, week_num_start, week_num_end):
        """
        Gets a summary from start to end week (end week number is included)
        :return: dictionary of [tile]:[reports for this tile]
        """
        from leaderboard.models.reportweeks import get_reportweek_class
        # TODO this hits the db once for each week number, consider refactor
        result = {}
        for i in range(week_num_start, week_num_end + 1):
            reports_for_week = getattr(self, get_reportweek_class(i).__tablename__)
            for wk in reports_for_week:
                if wk.tile not in result:
                    result[wk.tile] = []
                result[wk.tile].extend([wk])

        # TODO more than just obs count may be supported in future (wifi count, cell counts)
        return result

    def get_report_for_current_week(self):
        from leaderboard.models.reportweeks import current_week_number
        w = current_week_number()
        return self.get_report_counts_for_weeks(w, w)
