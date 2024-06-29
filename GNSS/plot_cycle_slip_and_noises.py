import matplotlib.pyplot as plt 
import base as b 
import PlasmaBubbles as pb 
import datetime as dt
import pandas as pd
import numpy as np


b.config_labels()


def load_data(dn, root = 'E:\\', sector = -50):
    
        
    out = []
    for day in range(2):
        delta = dt.timedelta(days = day)
    
        path = pb.path_roti(dn + delta, root = root)
        
        out.append(b.load(path))
        
    df = b.sel_times(pd.concat(out), dn, hours = 16)
    
    return pb.filter_region(df, dn.year, sector)
    
   


def dumb_data():
    times = pd.date_range(
        '2013-12-24 21:00', 
        '2013-12-24 21:04', 
        periods=20
        )
   
    data = {'roti': np.random.uniform(0, 1, len(times)), 
            'el': np.ones(len(times)) + 32}
    return pd.DataFrame(data, index = times)




dn = dt.datetime(2013, 12, 24, 18)
df = load_data(dn)

df = df.loc[df['sts'] == 'salu']
df = pd.concat([df, dumb_data()]).sort_index()


def plot_cycle_slip_and_noises(df):
        
    fig, ax = plt.subplots(
        nrows = 2,
        dpi = 300,
        sharey = True, 
        sharex = True, 
        figsize = (12, 10)
        
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    
    ax[0].plot(df['roti'])
    
    ds = df.loc[(df['el'] >  30) & (df['roti']<  5)]
    
    ax[-1].plot(ds['roti'])
    
    
    ax[0].set(
        ylim = [0, 6], 
        ylabel =  'ROTI (TECU/min)')
    
    ax[-1].set(
        ylim = [0, 6], 
        ylabel =  'ROTI (TECU/min)'
        )
    
    xy = (dt.datetime(2013, 12, 24, 21), 1)
    xytext = (dt.datetime(2013, 12, 24, 19), 2)
    
    ax[-1].annotate(
        'Possível\nperda de ciclo', xy=xy, 
        xytext=xytext,
        arrowprops=dict(arrowstyle='->'), 
        transform = ax[-1].transData, 
        fontsize = 20)
    
    ax[0].text(
        0.01, 0.85, '(a) Todas elevações', 
               transform = ax[0].transAxes)
    
    
    ax[1].text(
        0.01, 0.85, 
        '(a) Apenas maiores que 30$^\circ$', 
               transform = ax[1].transAxes)
    
    b.format_time_axes(ax[-1])
    
    return fig 


    
fig =  plot_cycle_slip_and_noises(df)

FigureName = 'cicle_slip_demo'


fig.savefig(
      b.LATEX(FigureName, folder = 'timeseries'),
      dpi = 400
      )