import pandas as pd
import numpy as np
import datetime as dt 
import base as b 
import matplotlib.pyplot as plt 

def load_tec(infile, values = True):

    df = pd.read_csv(
        infile, 
        delimiter = ';', 
        header = None
        ).replace(-1, np.nan)
    
    xmax, ymax = df.values.shape
   
    df.columns = np.arange(0, ymax)*0.5 - 90
    df.index = np.arange(0, xmax)*0.5 - 60
    
    if values:
        return df.columns, df.index, df.values
    else:
        return df

# sel = df.loc[
#      ((df.index > -10) & (df.index < 10)), 
#      (df.columns > -50) & (df.columns < -40)
#        ]

# return np.nanmean(sel.values)

def load_from_dn(dn, root = 'E:\\'):
    
    path = b.get_path(dn, root = root)
        
    return load_tec(path, values = False) 


def stack_tec(dn):
    root = 'E:\\'
    dn_min = b.closest_datetime(
        b.tec_dates(dn, root = root), dn)
    
    infile = b.get_path(dn_min, root = root)
    
    df = load_tec(infile, values = False)
    
    return (
        df.stack()                  # converte grade 2D → série (lat, lon)
          .reset_index()            # vira dataframe
          .rename(columns={
              'level_0': 'lat',
              'level_1': 'lon',
              0: 'tec'
          })
    )

def convert_to_mag(df, time, alt_km=350):
    import apexpy
    mlat = []
    mlon = []
    tec  = []
    

    for row in df.itertuples(index=True):
        lat = row.lat
        lon = row.lon
        tec_value = row.tec      # sua coluna TEC

        apex = apexpy.Apex(date=2015)
        a, b = apex.convert(lat, lon, 
                            'geo', 'qd', height = 300)
        mlat.append(a)
        mlon.append(b)
        tec.append(tec_value)

    return pd.DataFrame({
        "mlat": mlat,
        "mlon": mlon,
        "tec": tec
    })

def mean_by_bins(df):
    lat_bins = np.arange(df.mlat.min(), df.mlat.max() + 0.5, 0.5)
    lon_bins = np.arange(df.mlon.min(), df.mlon.max() + 0.5, 0.5)
    
    df["lat_bin"] = pd.cut(
        df.mlat, bins=lat_bins, labels=lat_bins[:-1])
    
    df["lon_bin"] = pd.cut(
        df.mlon, bins=lon_bins, labels=lon_bins[:-1])
    
    return (
        df.groupby(["lat_bin", "lon_bin"])["tec"]
          .mean()
          .reset_index()
          .rename(columns={"lat_bin": "mlat", "lon_bin": "mlon"})
    ).dropna().astype(float).round(2)

import matplotlib.pyplot as plt 


dn = dt.datetime(2015, 12, 19, 22)

df = stack_tec(dn)
df = convert_to_mag(df, dn, alt_km=350)



ds = mean_by_bins(df)

df1 = ds.pivot(index="mlat", columns="mlon", values="tec") 
plt.contourf(
    df1.columns, 
    df1.index, 
    df1.values, 
    30, 
    cmap = 'jet'
    )

ss = ds.loc[ds.mlon == 15.98]

# plt.plot(ss.mlat, ss.tec)