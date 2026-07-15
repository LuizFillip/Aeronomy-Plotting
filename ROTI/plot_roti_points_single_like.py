import epbs as pb 
import datetime as dt 
import plotting as pl 
import matplotlib.pyplot as plt 
import base as b 
import GEO as gg 
import pandas as pd 
import numpy as np 
import matplotlib.dates as mdates


def load_and_filter(dn, root = 'D:\\'):
 
    df = pb.get_nighttime_roti(dn, root = root, hours = 10)
     
    stations = ['rnmo', 'pbcg', 
                'pepe', 'recf', 
                'rnna', 'pbjp']
    
    df = df.loc[df['sts'].isin(stations)]
    
    # df = df.loc[
    #     (df.lon > -40) & 
    #     (df.lon < -35) & 
    #     (df.lat > -10) & 
    #     (df.lat < -5)
    #     ]
    
    return df


def single_roti(dn):
  
    df = load_and_filter(dn, root = 'D:\\')
     
    fig, ax = plt.subplots(
        figsize = (10, 5)
        )
    
    pl.plot_roti_timeseries(
            ax, 
            df,  
            ref_long = None
            )
    
    lat, lon = gg.sites['ca']['coords']
    dusk = gg.dusk_time(
            dn,  
            lat = lat, 
            lon = lon, 
            twilight = 18,
            suni = 'dusk'
            )

    
    ax.axvline(dusk, lw = 2, color = 'k')
    pb.short_epb_features(pb.process_max_events(df))
    
    return fig 
    


def plot_contour_roti(ax, vmax = 5, col_roti = '-50'):
    df = b.load('database/epbs/roti/maximums_roti2')
    mask = df.index.month.isin([5, 6, 7, 8])
  
    df.loc[mask,  col_roti] *= 0.5 
    df.loc[df['time'] < 20, 'time'] += 24 
    
    df['date'] = pd.to_datetime(df['date'])
   
    ds = pd.pivot_table(
        df,
        index = 'time', 
        columns = 'date', 
        values =  col_roti
        ) 
    values =  ds.values
    
    values = np.where(values > vmax, vmax, values)
    
    img = ax.contourf(
        ds.columns, 
        ds.index, 
        values,
        levels = np.arange(0,  vmax, 0.2), 
        cmap = 'turbo'
        )
    
    ax.set(
        yticks = np.arange(21, 36, 3)[:-1],
        ylim = [20, 32],
        yticklabels = ['18', '21', '00', '03'],
        ylabel = 'Local Time', 
        xlim = [df['date'].min(), df['date'].max()], 
        )
    
    

    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    ticks = np.arange(0, vmax + 5, 1)
    
    cax = ax.inset_axes([1.05, 0., 0.03, 1])

    cb = plt.colorbar(
        img, 
        cax = cax,
        ticks = ticks, 
        location = 'right'
        )
     
    cb.set_label('ROTI (TECU/min)')
 

    return None


df = b.load('database/epbs/roti/maximums_roti2')

 
#%%%%
ds = df.loc[(df['time'] > 20) & (df['time'] < 23)]


ds = ds['-50'].resample('D').mean().to_frame()
ds['year'] = ds.index.year 
ds['doy'] = ds.index.day_of_year 


ds = ds.pivot(values = '-50', columns = 'year', index = 'doy')

ds.mean(axis = 1).plot()
