import pg8000

template_get_name = """
SELECT
    name
FROM
    country_bounds
WHERE
    ogc_fid=%d
    """

#mpl = """
#SELECT
#    *
#FROM
#    country_bounds
#WHERE
#    cells.the_geom &&
#    ST_Transform(ST_MakeEnvelope( %(lon1)0.7f, %(lat1)0.7f,
#                                  %(lon2)0.7f, %(lat2)0.7f, 4326),
#                                  4326)
#LIMIT 1000
#    """

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
    #cols = None
    #ret = []
    #for row in cursor:    
        #if cols is None:
        #    cols = [d[0] for d in cursor.description]
        #rdict = dict(zip(cols, row))
        #del rdict['the_geom']
        #ret.append(rdict)
    #return ret

