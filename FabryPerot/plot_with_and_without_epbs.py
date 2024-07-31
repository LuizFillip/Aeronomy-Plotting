import base as b
import numpy as np
import datetime as dt 
import pandas as pd


def ones_data(dn):
    start = dn.replace(hour = 21)
    end = start + dt.timedelta(hours = 10)
    # df_source = c.geo_index()
    # df['dst'] = df.index.map(df_source['dst'])
    
    
    index = pd.date_range(start, end, freq = '10min')
    
    return pd.DataFrame({'epb': np.ones(len(index))}, index = index)

def adding_epb_occurrence(df):
    
    ds = b.load('events_class2')
    ds = ds.loc[
        (ds['type'] == 'sunset') &
        (ds['drift'] == 'fresh') &
        (ds['lon'] == -50)]

    out = []
    for dn in ds.index:
        out.append(ones_data(dn))
        
    ds1 = pd.concat(out)
    
    df['epb'] = df.index.map(ds1['epb'])
    
    df['epb'] = df['epb'].replace(float('nan'), 0)
    
    return df 
