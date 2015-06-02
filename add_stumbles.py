import json
import pg8000

with open('../db_connect_params.json') as f:
   db_params = json.load(f)

conn = pg8000.connect(user=db_params['user'],
                      password=db_params['password'],
                      database=db_params['database'])

key_grid = 'tile'
key_cellcount = 'cellcount'
key_wificount = 'wificount'

def add_stumbles_for_user(email, login_token, query_json):
    grid_num = query_json[key_grid]
    cellcount = query_json[key_cellcount]
    wificount = query_json[key_wificount]

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

