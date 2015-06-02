import pg8000
import math

mercator_id = 3857 # http://en.wikipedia.org/wiki/Web_Mercator 3785 # 900913 or 3857
wgs84_id = 4326

# Code from here, http://wiki.openstreetmap.org/wiki/Mercator
# spherical world mercator (not elliptical)
earth_radius = 6378137.000

def lat2y_m(lat):
    return earth_radius * math.log(math.tan(math.pi/4 + math.radians(lat) / 2))

def lon2x_m(lon):
    return math.radians(lon) * earth_radius

def get_easting_northing(lon, lat):
    conn = pg8000.connect()
    curs = conn.cursor()
    q = "SELECT ST_AsText(ST_Transform(ST_SetSRID(ST_POINT(%f, %f), %d), %d))" % \
                 (lon, lat, wgs84_id, mercator_id)
    curs.execute(q)
    easting, northing = curs.fetchone()[0].replace('POINT(', '').replace(')', '').split()
    return float(easting), float(northing)

def postgres_wgs84_coord_to_mercator(lng_lat_string):
    geo = "ST_GeomFromText('%s', %d)" % (lng_lat_string, mercator_id)
    transform = "ST_Transform(%s, %d)" % (geo, wgs84_id)
    return transform

