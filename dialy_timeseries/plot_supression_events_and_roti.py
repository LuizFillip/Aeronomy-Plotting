import datetime as dt 
import core as c 
import matplotlib.pyplot as plt
import base as b 
import PlasmaBubbles as pb 
import pandas as pd 
import numpy as np 

PATH_EPB = 'database/epbs/longs/'
PATH_DST = 'database/indices/omni_hourly.txt'

b.config_labels()



def plot_roti(ax, start, end, root = 'E:\\'):
    
    out = []
    for dn in pd.date_range(start, end):
        
        path = pb.path_roti(dn, root = root)
    
        out.append(
            pb.load_filter(path, remove_noise = True))
    
    
    df = pd.concat(out)
    df = df.loc[df['sts'].isin(['salu', 'pbjp'])]
    
    ds = b.sel_dates(df, start, end)
    
    ax.scatter(
        ds.index, ds['roti'], 
        c = 'k', s = 5, 
        alpha = 0.6)
    ax.set(
        xlim = [ds.index[0], ds.index[-1]],
        ylim = [0, 6], 
        yticks = np.arange(0, 6, 1)
        )
    
    return None 


def plot_dst(ax, dn, start, end):
    
    df = b.load(PATH_DST)
    df = b.sel_dates(df, start, end)
    
    ax1 = ax.twinx()
    
    ax1.plot(df['dst'], color = 'r')
    
    b.change_axes_color(
            ax1, 
            color = 'red',
            axis = "y", 
            position = "right"
            )
    
    start = dn + dt.timedelta(hours = 21)
    
    ax.axvspan(
        start, 
        start + dt.timedelta(hours = 12), 
        ymin = 0, 
        ymax = 1,
        alpha = 0.2, 
        color = 'gray'
        )
    
    ax1.set(
        ylim = [-300, 100], 
        yticks = np.arange(-300, 100, 100), 
        )
    ax1.axhline(0, linestyle = '--', color = 'red')
    
    return None

def plot_dialy_roti_and_dst(
        days,
        translate = False, 
        fontsize = 30, 
        nrows = 4
        
        ):
    
    if translate:
        xlabel = 'Days'
    else:
        xlabel = 'Dias'
    
    
    fig, ax = plt.subplots(
        nrows = nrows, 
        dpi = 300, 
        figsize = (12, 10),
        sharey = True
        )
    
    
    plt.subplots_adjust(hspace = 0.25)
    
   
    for i, dn in enumerate(days[:nrows]):
        
        start = dn - dt.timedelta(days = 2)
        end = dn + dt.timedelta(days = 4)
        
        plot_roti(ax[i], start, end, root = 'E:\\')
       
        plot_dst(ax[i], dn, start, end)
        
        b.format_days_axes(ax[i])
        
        month = b.monthToNum(dn.month, language = 'pt')
        
        l = b.chars()[i]
        
        s = f'({l}) {month}, {dn.year}'
        
        ax[i].text(
            0.02, 0.8, s, 
            transform = ax[i].transAxes
            )
    
    ax[-1].set(xlabel = xlabel)
    
    fig.text(
        0.04, 0.36, 
        'ROTI (TECU/min)', 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.99, 0.4, 
        'Dst (nT)', 
        fontsize = fontsize, 
        rotation = 'vertical',
        color = 'r'
        )
    return fig 

df = c.atypical_frame(lon = -50, kind = 0, days = 3)
 
days = df.loc[df['dst'] < -90].index
 
fig = plot_dialy_roti_and_dst(days)

FigureName = 'supression_events'

fig.savefig(
      b.LATEX(FigureName, 'timeseries'),
      dpi = 400
      )
