import pandas as pd
import numpy as np
import datetime as dt 
import base as b 
import matplotlib.pyplot as plt 
import apexpy

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


def load_from_dn(dn, root = 'E:\\'):
    
    path = b.get_path(dn, root = root)
        
    return load_tec(path, values = False) 


def stack_tec(dn,  root = 'E:\\'):
   
    dn_min = b.closest_datetime(
        b.tec_dates(dn, root = root), dn)
    
    infile = b.get_path(dn_min, root = root)
    
    df = load_tec(infile, values = False)
    
    return (
        df.stack()                  
          .reset_index()            # vira dataframe
          .rename(columns={
              'level_0': 'lat',
              'level_1': 'lon',
              0: 'tec'
          })
    )

def convert_to_mag(df, time, alt_km=350):
   

    data = {
        "mlat": [],
        "mlon": [],
        "tec": []
    }

    for row in df.itertuples(index = True):
      
        apex = apexpy.Apex(date = time.year)
        mlat, mlon = apex.convert(
            row.lat, row.lon, 
            'geo', 'qd', height = alt_km
            )
        
        data['mlat'].append(mlat)
        data['mlon'].append(mlon)
        data['tec'].append(row.tec )
      
    
    return pd.DataFrame(data)

def mean_by_bins(df):
    lat_bins = np.arange(
        df.mlat.min(), 
        df.mlat.max() + 0.5, 0.5
        )
    lon_bins = np.arange(
        df.mlon.min(), 
        df.mlon.max() + 0.5, 0.5
        )
    
    df["lat_bin"] = pd.cut(
        df.mlat, bins=lat_bins, 
        labels = lat_bins[:-1])
    
    df["lon_bin"] = pd.cut(
        df.mlon, bins=lon_bins, 
        labels = lon_bins[:-1]
        )
    
    return (
        df.groupby(["lat_bin", "lon_bin"])["tec"]
          .mean()
          .reset_index()
          .rename(columns={"lat_bin": "mlat", "lon_bin": "mlon"})
    ).dropna().astype(float).round(2)



def load_madrigal(dn):
    fn = dn.strftime('gps%y%m%dg.002.hdf5.txt')
    df = b.load(fn)
    
    df = df.rename(columns = {'TEC': 'tec'})
    
    df = df.loc[
        (df.lon > -90) & (df.lon < -30) &
        (df.lat > -50) & (df.lat < 50) 
        ]
    
    df = convert_to_mag(df, dn)

    return mean_by_bins(df)
    
    

def sel_lon(ds, lon = 20, delta = 2):
    ss = ds.loc[(ds.mlon > lon) & (ds.mlon < lon + delta)]

    return ss[['mlat', 'tec']]

def interpolate(df, vmin = -40, vmax = 56, step = 0.5):
    df = df.sort_values('mlat')
    df = df.groupby('mlat', as_index=False).mean()   
    
    mlat_new = np.arange(vmin, vmax, step)
    
    tec_interp = np.interp(mlat_new, df['mlat'], df['tec'])
    data = {
        'mlat': mlat_new,'tec': tec_interp
    }
    return pd.DataFrame(data).set_index('mlat')

def run_in_days(lon = 20, delta = 2):
    out = []
    days = [13, 18, 29]
    for day in days:
        dn = dt.datetime(2015, 12, day, 22)
      
        out.append(
            interpolate(
                sel_lon(
                    load_madrigal(dn), 
                    lon = lon, 
                    delta = delta
                    )
                ).rename(columns = {'tec': day})
            )
        
    return pd.concat(out, axis = 1)

lon = 20
df = run_in_days(lon = lon) 

dn = dt.datetime(2015, 12, 20, 22)

ds = sel_lon(load_madrigal(dn), lon = lon).set_index('mlat')



def plot_magnetic_tec(df, ds):
    b.sci_format(fontsize = 25)
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (12, 6)
        )
    
    ax.plot(ds['tec'], lw = 2, label = 'Storm-time')
    
    avg = df.mean(axis = 1)
    std = df.std(axis = 1)
    
    ax.plot(avg, lw = 2, color = 'purple', label = 'Quiet-time')
    ax.fill_between(
        avg.index, 
        avg - std, 
        avg + std, 
        color = "purple", 
        alpha = 0.3
        )
    
    ax.set(
           xlabel = 'Magnetic latitude (°)',
           ylabel = 'TEC (TECU)',
           xlim = [-30, 30], 
           ylim = [0, 100],
           xticks = np.arange(-30, 30, 5)
           )
    
    ax.legend(loc = 'upper center', 
              ncol = 2)
    
    ax.axvline(0, linestyle = ':')
    
    return fig 
    
   

fig =  plot_magnetic_tec(df, ds)


def main():
    
    FigureName = 'latitude_tec_profile'
    
    path_to_save = 'G:\\Meu Drive\\Papers\\Case study - 21 december 2015\\June-2024-latex-templates\\'
    
    
    fig.savefig(path_to_save + FigureName, dpi = 400)
# import apexpy 

# apex = apexpy.Apex(date = 2015)

# apex.convert(
#     -2, -50, 
#     'geo', 'qd', height = 350
#     )
