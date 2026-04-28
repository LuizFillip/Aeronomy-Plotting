import epbs as pb 
import datetime as dt 
import plotting as pl 
import matplotlib.pyplot as plt 
import base as b 
import GEO as gg 
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
    


dn = dt.datetime(2014, 3, 2, 20)
# df = load_and_filter(dn, root = 'D:\\')
 
 

fig = single_roti(dn)

# path = 'database/epbs/cg_2009_2024'

# df = b.load(path)

# # df.loc[(df.index.month == dn.month) &
# #        (df.index.year == dn.year)]

# df.loc[dn.replace(hour = 0)]
 



