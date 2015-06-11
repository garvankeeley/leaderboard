import pg8000
import math
import coord_sys as cs

# Code from here, http://wiki.openstreetmap.org/wiki/Mercator
# spherical world mercator (not elliptical)
earth_radius = 6378137.000

def lat2y_m(lat):
    return earth_radius * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))

def lon2x_m(lon):
    return math.radians(lon) * earth_radius

def db_get_easting_northing(lon, lat):
    conn = pg8000.connect()
    curs = conn.cursor()
    q = "SELECT ST_AsText(%s)" % db_coord_transform(lon, lat, cs.WGS84_LATLON_CODE, cs.WEB_MERCATOR_CODE)
    curs.execute(q)
    easting, northing = curs.fetchone()[0].replace('POINT(', '').replace(')', '').split()
    return float(easting), float(northing)

def db_coord_transform_from_string(lng_lat_string, src_epsg, dest_epsg):
    geo = "ST_GeomFromText('%s', %d)" % (lng_lat_string, src_epsg)
    transform = "ST_Transform(%s, %d)" % (geo, dest_epsg)
    return transform

def db_coord_transform(lon, lat, src_epsg, dest_epsg):
    geo = "ST_SetSRID(ST_POINT(%f, %f), %d)" % (lon, lat, src_epsg)
    transform = "ST_Transform(%s, %d)" % (geo, dest_epsg)
    return transform


# def wgs84_string_coord_to_mercator(geo_string):
#     return db_coord_transform_from_string(geo_string, wgs84_id, mercator_id)
#
#
# def wgs84_coord_to_mercator(lon, lat):
#     return db_coord_transform(lon, lat, wgs84_id, mercator_id)