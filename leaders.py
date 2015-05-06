import pg8000

template_get_name = """
SELECT
    name
FROM
    country_bounds
WHERE
    ogc_fid=%d
    """

template_get_leaders = """
SELECT
  userinfo.name, weekly_report.observations
FROM
  weekly_report, userinfo, gridcell
WHERE
  gridcell.country_fk = %d AND
  weekly_report.userinfo_fk = userinfo.userinfo_pk AND
  gridcell.gridcell_pk = weekly_report.gridcell_fk
ORDER BY
  weekly_report.observations DESC
LIMIT 1000
"""


conn = pg8000.connect()
def fetch_leaders(query):
    cursor = conn.cursor()
    sql = template_get_name % query
    cursor.execute(sql)
    country_name = cursor.fetchone()[0]

    sql = template_get_leaders % query
    cursor.execute(sql)
    rows = [] # {{'name': x[0], 'observations': x[1]} for x in cursor}
    for row in cursor:
        rows.append({'name': row[0], 'observations': row[1]})

    result = {'country_name': country_name, 'leaders': rows}
    print result
    return result

