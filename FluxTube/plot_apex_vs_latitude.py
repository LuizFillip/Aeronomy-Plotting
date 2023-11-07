import matplotlib.pyplot as plt
import numpy as np
from FluxTube import Apex
import base as b
import pandas as pd 
import RayleighTaylor as rt
import os
import GEO as g
import datetime as dt



b.config_labels()



def plot_apex_vs_latitude(
        ax, 
       
        color = 'k'
        ):
    
    max_height = 400
    step = 50
    base = 75
    heights = np.arange(50, max_height + step, step )
     
   
    for h in heights:
        
        apx = Apex(h)
        lats =  apx.latitude_range(
            points = 30, 
            base = 150
            )
        apex = apx.apex_range(
            points = 30, 
            base = base
            )
        
        if h == 300:
            args = dict(
                marker = 'o', 
                markerfacecolor = color, 
                lw = 2)
        else:
            args = dict(color = 'k', lw = 2)
            
            
        ax.plot(np.degrees(lats), 
                apex, **args)    
        
    lim = 20
    ax.set(
        xlim = [-lim, lim],
        ylim = [base, max_height],
        ylabel = "Apex height (km)", 
        xlabel = "Magnetic latitude (°)"
        )
    
    ax.axvline(0, linestyle = "--")

        
    ax.axhline(
        150, 
        color = "red", 
        lw = 2,
        linestyle = "--"
        )
    
    x = -18
    fontsize = 35
    ax.text(x, 100, 'E region',
            transform = ax.transData, 
            fontsize = fontsize,
            color = 'w'
            )
    ax.text(x, 200, 'F region', 
            transform = ax.transData, 
            fontsize = fontsize,
            color = 'k'
            )
    
    ax.axhline(300, color = "k", lw= 2,
                linestyle = "--")
    
    ax.text(0.03, 0.91, '(b)', 
            transform = ax.transAxes, 
            fontsize = fontsize)
        
    return ax




def plot_contour(ax, dn, color, vmin, vmax):
    ax = plot_apex_vs_latitude(
        ax, color)
    
    
    ds1 = pd.pivot_table(
        df.loc[df['dn'] == dn] , 
        values = 'ne', 
        columns = 'glat', 
        index = 'alt_km'
        ) 
    
    levels = np.linspace(vmin, round(vmax), 20)
    img = ax.contourf(
        ds1.columns,
        ds1.index, 
        ds1.values, levels, 
        cmap = 'rainbow'
        )
    
    ticks = np.linspace(vmin, vmax, 5)
    
    b.colorbar_setting(
            img, 
            ax, 
            ticks, label = '$N_0 ~(cm^{-3})$'
            )
    
    
def plot_timeseries_GRT(ax):
    PATH_FLUXTUBE = "FluxTube/data/reduced/"
    
    year = 2013
    site = 'saa'
    infile = os.path.join(
        PATH_FLUXTUBE, 
        site, 
        f"{year}.txt"
        )
    ds = b.load(infile)
    
    dn = dt.datetime(2013, 1, 1, 20)
        
    df = rt.gammas_integrated(b.sel_times(ds, dn))
    
    df['gamma'] =  df['gamma'] * 1e3
    ax.plot(
        df['gamma'],
        lw = 2, 
        marker = 's', 
        fillstyle ='none')
    
    ax.set(
        ylim = [-0.2, 3], 
        ylabel = b.y_label('gamma'),
        xlim = [df.index[0], df.index[-1]]
        )
    
    F = g.dusk_from_site(dn, site, twilight_angle=18)
    
    ax.axvline(F, lw = 2)
    
    ax.text(F, 3.1, 'Terminator in 300 km', 
            transform = ax.transData)
    
    b.format_time_axes(ax)
    


def plot_iono(df, dn, color):
    
    df['ne'] = df['ne'] *1e-6

    
    vmax = df['ne'].max()
    vmin = df['ne'].min()

    fig, ax = plt.subplots(
        figsize = (18, 6), 
        ncols = 2,
        dpi = 300
        )   
        
    plot_timeseries_GRT(ax[0])
    delta = dt.timedelta(minutes = 10)
    
    n = pd.to_datetime(dn)
    ax[0].axvspan(
        n, n + delta,
        alpha = 0.7, 
        color = 'gray',
        edgecolor = 'k', 
        lw = 2
    )
    
    ax[0].text(0.01, 0.9, '(a)', fontsize = 35,
               transform = ax[0].transAxes)
    
    
    plot_contour(ax[1], dn, color, vmin, vmax)
    
    
    fig.suptitle(n.strftime('%H:%M (UT)'))
    
   
    
    return fig


def run_save(df):
    
    times = df['dn'].unique()
    
    plt.ioff()
    
    for i, dn in enumerate(times):
        
        print(dn)
        
        if i % 2 == 0:
            color = 'w'
        else:
            color = 'k'
            
        fig = plot_iono(df, dn, color)
        
        dn = pd.to_datetime(dn)
        Figurename  = dn.strftime('%Y%m%d%H%M')
        fig.savefig(f'models/temp/img/{Figurename}')
    
    plt.clf()   
    plt.close()
    
    
p = 'models/temp/iri.txt'

df = pd.read_csv(p)

# dn = df['dn'].unique()[12]



# fig = plot_iono(df, dn, color = 'k')

run_save(df)

