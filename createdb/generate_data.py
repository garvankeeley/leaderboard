import json
import sys
import os

import pg8000

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from geo_util import coord_utils


def create_random_users():
    conn = pg8000.connect()
    curs = conn.cursor()
    for i in range(0, 2000):
        try:
            curs.execute("INSERT INTO userinfo(name) VALUES ('%s')" % ('name' + str(i)))
            conn.commit()
        except pg8000.Error:
            print sys.exc_info()[0]
            conn.rollback()
            conn = pg8000.connect()
            curs = conn.cursor()

from random import randint
def create_some_tiles(coords):
    for coord in coords:
        lat = coord[1]
        lon = coord[0]
        if not isinstance(lat, float) or not isinstance(lon, float):
            print "bad lat lon: ", lat, lon
            return None

    geo = coord_utils.db_get_easting_northing(lon, lat)

        # cell = get_or_create_cell(coord)
        # if not cell:
        #    continue
        # for i in range(0, 5):
        #     user = get_user_pk('name' + str(randint(0, 1000)))
        #     #print cell, user
        #     try:
        #       insert_week(10, 2015, randint(10,100), user, cell)
        #     except pg8000.core.ProgrammingError as ex:
        #         print ex

def doit():
    with open('../geojson/world.geo.json') as data_file:
        data = json.load(data_file)
        for item in data['features']:
            print item['id']
            for c in item['geometry']['coordinates']:
                create_some_tiles(c)

#create_random_users()
#doit()

#p = (-9.4, 51.5)
#c = get_or_create_cell(p)

for i in range(0, 1000):
    a = randint(0, 85*2) - 85
    b = randint(0, 85*2) - 85
    e_m = coord_utils.lon2x_m(a)
    n_m = coord_utils.lat2y_m(b)
    #print a,b
    east, north = coord_utils.db_get_easting_northing(a, b)
    d1 = abs(n_m - north)
    d2 =  abs(e_m - east)
    if d1 + d2 > 0.001:
        print "error"




