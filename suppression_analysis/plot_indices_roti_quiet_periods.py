import numpy as np
import matplotlib.pyplot as plt
import plotting as pl 
import datetime as dt 
import PlasmaBubbles as pb 
import base as b 
import core as c
import GEO as gg 

bad = ['2013-09-24', '2013-11-10', '2015-09-20', '2015-10-08', '2016-03-29',
       '2017-09-24', '2018-02-14', '2018-11-23', '2019-02-24', '2019-10-17', 
       '2019-10-24', '2019-12-13', '2021-03-26', '2021-10-18', '2022-03-07', 
       '2022-04-02']

dub = ['2013-09-18', '2016-12-11', '2018-10-21', '2019-10-29', 
       '2021-03-23', '2022-09-19', '2022-09-20', '2022-12-28']


def plot_roti_in_range(ax, dn):


    ds = pb.longterm_raw_roti(dn, days = 1)
    
    ax.scatter(
        ds.index, 
        ds['roti'], 
        c = 'k', 
        s = 5, 
        alpha = 0.6
        )
    
    ax.set(
        ylabel = 'ROTI',
        ylim = [0, 5], 
        yticks = np.arange(0, 6, 1),
        xlim = [ds.index[0], ds.index[-1]]
        )
    
    return None 

def plot_indices_and_roti_longterm(dn):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (12, 10), 
        nrows = 4, 
        sharex = True
        )

    plt.subplots_adjust(hspace = 0.1)


    ds = c.high_omni(dn.year)
    pl.plot_auroras(ax[0], ds)
    pl.plot_magnetic_fields(ax[1], ds, ylim = 30)
    pl.plot_dst(ax[2], ds)

    plot_roti_in_range(ax[3], dn)
    
    ds = b.range_dates(ds, dn, days = 3)
    st = c.find_storm_interval(ds['sym'])
    
    
    for a in ax.flat:
        
        dusk = gg.terminator( -50,  dn, 
            float_fmt = False
            )
        a.axvline(
            dusk, 
            color = 'blue', 
            lw = 2, 
            linestyle = '--'
            )
        
        
        for line in st:
            
            a.axvline(line, color = 'red')
    
    devtime = (dusk - st[1]).total_seconds() / 3600
    devtime = round(devtime, 2)
    
    ax[-1].text(
        0, -0.35, f'Desviation: {devtime} hrs', 
        transform = ax[-1].transAxes
        )
    b.format_days_axes(ax[-1])
    
    b.plot_letters(
        ax, 
        y = 0.8, 
        x = 0.03, 
        num2white = None
        )
    
    ax[0].set(title = dn.strftime('%B, %Y'))
    
    fig.align_ylabels()
    
    return fig
import pandas as pd 

df = c.suppression_events(c.epbs(), days = 2)

df = df.loc[~(df.index.isin(pd.to_datetime(bad + dub)))]

# dn = df.index[1]

# fig = plot_indices_and_roti_longterm(dn)


def save_imgs(ds):
    from tqdm import tqdm 
    
    path = 'E:\\img\\'
    plt.ioff()
    
    for dn in tqdm(ds.index[30:]):
        try:
            fig = plot_indices_and_roti_longterm(dn)
            fig.savefig(path + dn.strftime('%Y%m%d'))
        except:
            continue
    
    plt.clf()   
    plt.close()
    
    
save_imgs(df)