import numpy as np
import matplotlib.pyplot as plt
import plotting as pl 
import datetime as dt 
import PlasmaBubbles as pb 
import base as b 
import core as c
import GEO as gg 


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

ds = c.suppression_events(c.epbs(), days = 2)

dn = ds.index[0]


def save_img():
    from tqdm import tqdm 
    
    path = 'E:\\img\\'
    plt.ioff()
    
    for dn in tqdm(ds.index):
        
        fig = plot_indices_and_roti_longterm(dn)
        fig.savefig(path + dn.strftime('%Y%m%d'))
        
    
    plt.clf()   
    plt.close()