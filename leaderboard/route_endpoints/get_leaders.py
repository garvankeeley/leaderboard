from decimal import Decimal
from geoalchemy2 import func
from leaderboard.models import reportweeks, contributor, tile, country_bounds
from leaderboard.db import session_factory
from sqlalchemy import desc


def get_leaders_for_country(country_id):
    week_class = reportweeks.get_current_reportweek_class()
    session = session_factory()
    q = session.query(contributor.Contributor,
                      func.sum(week_class.observation_count).label('obs_sum')).\
                      filter(tile.Tile.country_id == country_id).\
                      filter(week_class.contributor_id == contributor.Contributor.id).\
                      filter(week_class.tile_id == tile.Tile.id).\
                      group_by(contributor.Contributor.id).\
                      order_by(desc('obs_sum'))
    result = q.all()
    if result:
        assert isinstance(result[0][0], contributor.Contributor)
        assert isinstance(result[0][1], Decimal)

    rows = []
    for row in result:
        rows.append({'name': row[0].nickname,
                     'observations': str(row[1])})

    country_name = session.query(country_bounds.CountryBounds.name).\
        filter_by(ogc_fid=country_id).first()

    return {'country_name': country_name, 'leaders': rows}
