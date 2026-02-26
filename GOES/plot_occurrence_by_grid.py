import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import base as b
import GEO as gg

 
 
def classify_lat(lat):
    if abs(lat) <= 23.5:
        return "Tropical"
    elif abs(lat) <= 35:
        return "Subtropical"
    else:
        return "Extratropical"

# df["lat_sector"] = df["lat_center"].apply(classify_lat)

def join_ep_cloud(df, ds, col):
    df1 = pd.concat([df[col], ds[col]], axis = 1).dropna()
    
    x = df1.iloc[:, 0].values
    y = df1.iloc[:, 1].values
    
     
    fig, ax = plt.subplots()
    
    ax.plot(df1.iloc[:, 0])
    ax1 = ax.twinx()
    
    ax1.plot(df1.iloc[:, 1], color = 'b')
    
    np.corrcoef(x, y)[0, 1]
    
def latitudinal_bins_cloud(df):
    
    bins = np.arange(-60, 10, 10)
    
    df["lat_sector"] = pd.cut(df["lat"], bins=bins)
    
    df = df.groupby(["lat_sector"]).size()
    
    ds = df.unstack("lat_sector")
    
    ds.columns = bins[:-1]
    
    # ds.index = pd.to_datetime(ds.index)

    # ds.index = ds.index.to_period("M").to_timestamp()
    
    return ds 

    
import GOES as gs 

def latitudinal_bins_waves(year = 2013, col = "mean_90_110"):
  
    df = gs.potential_energy(year = year)
    
    bins = np.arange(-60, 10, 10)
     
    df["lat_sector"] = pd.cut(df["lat"], bins=bins)
    
    df = df.dropna()
    
    mean_cols = [c for c in df.columns 
                 if c.startswith("mean")]
    
    df = (
        df[mean_cols + ["lat_sector"]]
          .groupby("lat_sector")
          .resample("1H")
          .mean(numeric_only=True)
    )
    
    df = df[col].unstack("lat_sector").fillna(np.nan)
    df.columns = bins[:-1]
    return df
def join_years_ep():
    out = []
    for year in range(2013, 2018):
        out.append(latitudinal_bins_waves(year))
    
   
    return pd.concat(out)

df = b.load("nucleos_2012_2018") 

lon_col=("lon_min", "lon_max")
lat_col=("lat_min", "lat_max")
 
df["lon"] = (df[lon_col[0]] + df[lon_col[1]]) / 2.0
df["lat"] = (df[lat_col[0]] + df[lat_col[1]]) / 2.0


print(df)


df = df.loc[(df.lon > -80) & (df.lon < -40)]

# ds = latitudinal_bins_cloud(df)

bins = np.arange(-60, 10, 10)

df["lat_sector"] = pd.cut(df["lat"], bins=bins)

 
df['occ'] = 1

df = (
    df
    .groupby([pd.Grouper(freq="3H"), "lat_sector"])["occ"]
    .sum()
    .unstack("lat_sector")
    .fillna(np.nan)
)

df.columns = bins[:-1]

df = (df / df.sum()) * 100

df = df.replace(0, np.nan).interpolate()

df.plot(subplots = True, figsize = (12, 12))

