import json
import pg8000
import datetime

template_create_week = """
CREATE TABLE %(table_name)s (
    %(pk_name)s bigserial NOT NULL,
    observations int,
    discovery_cells int,
    discovery_observation int,
    userinfo_fk bigint  NOT NULL,
    tile_fk bigint  NOT NULL,
    CONSTRAINT WEEKLY_REPORT_pk PRIMARY KEY %(pk_name)s
);
CREATE UNIQUE INDEX %(table_name)s_UNIQUE_USER_FOR_TILE ON %s(userinfo_fk, tile_fk);
ALTER TABLE %(table_name)s ADD CONSTRAINT %(table_name)s_TILE_FK
    FOREIGN KEY (tile_fk)
    REFERENCES tile (tile_pk)
    NOT DEFERRABLE
    INITIALLY IMMEDIATE
;
ALTER TABLE WEEKLY_REPORT ADD CONSTRAINT %(table_name)s_USER_FK
    FOREIGN KEY (userinfo_fk)
    REFERENCES USERINFO (userinfo_pk)
    NOT DEFERRABLE
    INITIALLY IMMEDIATE
;
"""

with open('../db_connect_params.json') as f:
   db_params = json.load(f)

def connect():
    return pg8000.connect(user=db_params['user'],
                      password=db_params['password'],
                      database=db_params['database'])

def insert_or_update_week(is_update, obs, userpk, tilepk):
    conn = connect()
    curs = conn.cursor()

    keys = ('userinfo_pk', 'tile_pk', 'observations')
    values = (userpk, tilepk, obs)

    if is_update:
        update_template = 'update %(table_name)s set %(key_values)s where ' \
                          'userinfo_fk=%(userinfo_fk)d and tile_fk=%(tile_fk)d'
        query = update_template % {'table_name': weekly_table_name(),
                                   'keys': ",".join(keys),
                                   'values': ','.join(values)}
    else:
        insert_template = "insert into %(table_name)s(%(keys)s) values(%(values)s)"
        query = insert_template % {'table_name': weekly_table_name(),
                                   'key_values': str(zip(keys, values))[1:-1],
                                   'userinfo_fk': userpk,
                                   'tile_fk': tilepk}
    try:
        curs.execute(query)
        conn.commit()
    except pg8000.Error as ex:
        print ex

def get_week_table_stats(userpk, tilepk):
    query = 'select observations from %s where userinfo_fk=%d and tile_pk=%d' % \
               (weekly_table_name(), userpk, tilepk)

    conn = connect()
    curs = conn.cursor()
    try:
        curs.execute(query)
    except pg8000.Error:
        return None
    # TODO fill this in properly
    return curs.fetchone()[0]

def weekly_table_name():
    return "WEEK_%d_PER_TILE_PER_USER" % week_num_of_year()

def week_num_of_year():
    return datetime.datetime.now().isocalendar()[1]

def year_and_month_num():
    now = datetime.datetime.now()
    return "%d%d" % (now.year, now.month)

