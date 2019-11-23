import pandas as pd
import numpy as np
import fiona


"""Functions to parse shape file and create count df"""
def create_loc_counts_df(loc,taxi_zones_path):
    loc_count = loc.value_counts()
    zones_coord_dict = get_zones_coord(taxi_zones_path)
    df = parse_centriod_count(loc_count,zones_coord_dict)
    return df 

def get_zones_coord(taxi_zones_path):
    zones_coord_dict = {}
    with fiona.open(taxi_zones_path, 'r') as shape:
        while True:
            try:
                poly = shape.next()
                poly_id = poly['id']
                poly_coords = poly['geometry']['coordinates'][0]
                centroid = find_centroid(poly_coords)
                zones_coord_dict[poly_id] = centroid
            except:
                return zones_coord_dict
            
def parse_centriod_count(counts,zones_coord_dict):
    lat_list = []
    lon_list = []
    count_list = []
    id_list = []
    for poly_id, count in counts.items():
        try:
            lon,lat = zones_coord_dict[str(poly_id)]
            id_list.append(str(poly_id))
            lat_list.append(lat)
            lon_list.append(lon)
            count_list.append(count)
        except:
            continue
    df_dict ={
        'id':id_list,
        'latitude':lat_list,
        'longitude':lon_list,
        'count': count_list
    }
    df = pd.DataFrame.from_dict(df_dict)
    return df


def find_centroid(poly_coords):
    lat, long = 0,0
    if len(poly_coords) < 2:
        poly_coords = poly_coords[0]
    for coord in poly_coords:
        lat += coord[0]
        long += coord[1]
    lat_cent = lat/len(poly_coords)
    long_cent = long/len(poly_coords)
    return (lat_cent,long_cent)