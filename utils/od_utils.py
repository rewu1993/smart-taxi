import pandas as pd
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt
from pyproj import Proj, transform

'''Codes for ploting topn graphs'''
def translate_zone_code(zone_df,code):
    return zone_df[zone_df['LocationID']==code]['Zone'].item()

def get_topn_pu(n,pu_count_df):
    top_pu = pu_count_df[:n]
    return top_pu['id']

def get_topn_do_from_pu(n,pu_id,od):
    d = od[pu_id]
    return sorted(range(len(d)), key=lambda i: d[i])[-n:]
    
def create_empty_df(column_names):
    df = pd.DataFrame(columns=column_names)
    return df
        
def translate_loc_names(do_ids,zone_df):
    do_names = []
    for do_id in do_ids:
        do_names.append(translate_zone_code(zone_df,do_id))
    return do_names

def create_topn_od(n,pu_count_df,od,zone_df):
    top_pu = get_topn_pu(n,pu_count_df)
    column_names = ['pu_id']+[i+1 for i in range(n)]
    top_df = create_empty_df(column_names)
    for i,pu_id in enumerate(top_pu):
        top_do = get_topn_do_from_pu(n,pu_id,od)
#         top_do_names = translate_loc_names(top_do,zone_df)
        top_df.loc[i] = [pu_id]+ top_do
    return top_df
def parse_plot_info(row,pu_count_df,zone_df):
    inProj  = Proj("+init=EPSG:2263",preserve_units=True)
    outProj = Proj("+init=EPSG:4326") # WGS84 in degrees and not EPSG:3857 in meters
    
    loc_idxs = list(row)
    loc_names = translate_loc_names(loc_idxs,zone_df)
    lats,longs = [],[]
    for loc_id in loc_idxs:
        r = pu_count_df[pu_count_df['id'] == loc_id]
        lat,long = transform(inProj,outProj,r.longitude.item(),r.latitude.item())
        lats.append(lat)
        longs.append(long)
    return lats,longs,loc_names

def plot_pu_do(lat,long,loc_names,save_path):
    plt.figure(figsize=(14, 8))
    font = {'family' : 'normal',
        'size'   : 18}
    plt.rc('font', **font)
    for i,type in enumerate(loc_names):
        x = lat[i]
        y = long[i]
        if i ==0 :
            plt.scatter(x, y, marker='o',s=200, color='yellow')
        else:
            plt.scatter(x, y, marker='x', color='red')
        plt.text(x+0.001, y+0.001, type, fontsize=14)
    plt.gca().invert_yaxis()
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    if save_path:
        plt.savefig(save_path)
    plt.show()