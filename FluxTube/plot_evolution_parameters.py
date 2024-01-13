import pandas as pd 
import RayleighTaylor as rt
import os
import GEO as g
import datetime as dt

from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator


def shade_interval(ax, dn):
    delta = dt.timedelta(minutes = 10)
    
    n = pd.to_datetime(dn)
    
    ax.axvspan(
        n, n + delta,
        alpha = 0.7, 
        color = 'gray',
        edgecolor = 'k', 
        lw = 2
    )
    
    ax.text(
        0.01, 0.9, '(a)', 
        fontsize = 35,
        transform = ax.transAxes
        )

def plot_contour(ax, ds1, vmin, vmax, color =  'k'):
    ax = plot_apex_vs_latitude(ax, color)
    
    levels = MaxNLocator(nbins = 100).tick_values(vmin, vmax)
    cmap = plt.get_cmap('rainbow')
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    
    img = ax.pcolormesh(
        ds1.columns,
        ds1.index, 
        ds1.values, 
        norm  = norm,
        cmap = cmap
        )
    
    plt.colorbar(img)
    
    
def plot_timeseries_GRT(ax, site = 'saa', year = 2013):
    PATH_FLUXTUBE = "FluxTube/data/reduced/"
    
    infile = os.path.join(
        PATH_FLUXTUBE, 
        site, 
        f"{year}.txt"
        )
    ds = b.load(infile)
    
    dn = dt.datetime(2013, 1, 1, 20)
        
    df = rt.gammas_integrated(b.sel_times(ds, dn, hours = 11))
    
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
    E = g.dusk_from_site(dn, site, twilight_angle=0)
    ax.axvline(F, lw = 2)
    ax.axvline(E, lw = 2)
    
    ax.text(F, 3.1, 'Terminator in 300 km', 
            transform = ax.transData)
    
    b.format_time_axes(ax)
    
def set_data(df, dn):
    
    return pd.pivot_table(
        df.loc[df['dn'] == dn] , 
        values = 'ne', 
        columns = 'glat', 
        index = 'alt_km'
        ) 
    


def plot_contour_field_lines(df, dn, color = 'k'):

    fig, ax = plt.subplots(
        figsize = (18, 6), 
        ncols = 2,
        dpi = 300
        )   
        
    plot_timeseries_GRT(ax[0])

    shade_interval(ax[0], dn)

    plot_contour(
        ax[1], set_data(df, dn),
        vmin, vmax, color = color)

    n = pd.to_datetime(dn)
    fig.suptitle(n.strftime('%H:%M (UT)'))
        
    return fig, n.strftime('%Y%m%d%H%M')

def run():  
    df = pd.read_csv('models/temp/iri.txt')
    
    df = df.replace(-1, np.nan)
    
    df['ne'] = df['ne'] *1e-6
    
    vmin = df['ne'].min()
    vmax = df['ne'].max()
    
    
    for i, dn in enumerate(df['dn'].unique()):
        
        print(dn)
        
        if i % 2 == 0:
            color = 'w'
        else:
            color = 'k'
            
        fig, name = plot_contour_field_lines(df, dn, color)
        
        fig.savefig(f'models/temp/img/{name}')
