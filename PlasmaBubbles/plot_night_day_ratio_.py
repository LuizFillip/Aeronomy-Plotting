import PlasmaBubbles as pb
import matplotlib.pyplot as plt 
import base as b 
import datetime as dt 
import os 
import numpy as np

b.config_labels()

args = dict(
    marker = 'o', 
    markersize = 3,
    linestyle = 'none', 
    alpha = 0.5,
    color = 'k'
    )


def plot_std_shade(ax, df, i = 3):
    
    ax.fill_between(
        df.index, 
        df['avg'] + i * df['std'], 
        df['avg'] - i * df['std'], 
        alpha = 0.3, 
        color = 'r'
        )
    

def shade_area(
        ax, 
        start,
        name = 'Daytime', 
        color = '#0C5DA5'
        ):

    end = start + dt.timedelta(hours = 8)
    
    ax.axvspan(
        start, end, 
        ymin = 0, ymax = 0.71,
        alpha = 0.2, 
        color = color
        )
    
    delta = dt.timedelta(hours = 1.5)
    middle = start + (end - start) / 2 
    
    ax.text(
        middle - delta, 
        0.75, 
        name, 
        transform = ax.transData
        )


receivers = [
    'pepe',
     'mabb',
     'mabs',
     'crat',
     'topl',
     'maba',
    'pitn',
     'picr',
     'brft',
     'ceft',
     'ceeu',
     'salu',
     'impz']




def plot_stats_shade(
        ax, ds, dn, 
        st = 12, 
        et = 20,
        color = 'gray'
        ):
    
    d = ds.between_time(
        f'{st}:00', 
        f'{et}:00'
        )
    
    d_avg = np.mean(d['roti'])
    d_avg = round(d_avg, 3)
    
    ref_time = d.index[0].time()
    
    if ref_time >= dt.time(21, 0):
        title = 'Nighttime' 
    else:
        title = 'Daytime'
    
    shade_area(
            ax, 
            dn,
            name = f'{title}\n$\mu$ = {d_avg}', 
            color = color
            )
    
    
def plot_roti_timeseries(ax, df, dn):
    
    df = df.loc[df['sts'].isin(receivers)]

    ds = b.sel_times(df, dn, hours = 17)

    ax.plot(ds['roti'], **args)
    
    plot_stats_shade(
        ax, ds, dn, 
        st = 12, 
        et = 20,
        color = '#0C5DA5'
        )
    
    delta = dt.timedelta(hours = 9)
    
    plot_stats_shade(
            ax, ds, dn + delta, 
            st = 21, 
            et = 5,
            color = 'gray'
            )
    
 
    b.format_time_axes(ax, hour_locator = 2)
    
    ax.set(
        ylabel = 'ROTI (TECU/min)',
        ylim = [0, 2], 
        xlim = [ds.index[0], ds.index[-1]]
        )

def plot_night_day_ratio(dates):
    
    fig, ax = plt.subplots(
        dpi = 300,
        nrows = 2, 
        ncols = 2,
        sharey = True,
        figsize = (14, 10)
        )
    
    plt.subplots_adjust(
        hspace = 0.4, 
        wspace = 0.05
        )
    
    names = ['Solar maximum (summer)', 
             'Solar minimum (summer)', 
             'Solar maximum (winter)' , 
             'Solar minimum (winter)']
    
    for i, ax in enumerate(ax.flat):
        
        dn = dates[i]
        n = names[i]
        
        df = pb.concat_files(
            dn, pb.load_filter, 
            os.getcwd()
            )
        
        plot_roti_timeseries(ax, df, dn)
        
        l = b.chars()[i]
        ax.text(
            0.03, 0.85, f'({l}) {n}', 
            transform = ax.transAxes
            )
        
        if (i == 1) or (i == 3):
            ax.set(ylabel = '')
    
    fig.suptitle('Days without EPB', y = 0.93)
    
    return fig


# dates = [
#          dt.datetime(2013, 3, 17, 12),
#          dt.datetime(2019, 1, 11, 12),
#          dt.datetime(2013, 6, 1, 12),
#          dt.datetime(2019, 6, 1, 12)
         
#          ]


# fig = plot_night_day_ratio(dates)