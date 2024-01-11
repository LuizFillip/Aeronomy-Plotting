import cartopy.crs as ccrs
import GEO as gg
import matplotlib.pyplot as plt
import datetime as dt 
from matplotlib.gridspec import GridSpec
import plotting as pl
import base as b
import PlasmaBubbles as pb 
import numpy as np 

b.config_labels(fontsize = 25)

def range_time(start, mi):
        
    return start + dt.timedelta(minutes = mi)

def multi_layout(nrows = 4):
    
    fig = plt.figure(
        dpi = 300, 
        figsize = (18, 7)
        )
    
    gs = GridSpec(nrows, 8)
    
    plt.subplots_adjust(wspace = 3, hspace = 0.1)
    
    ax_map = fig.add_subplot(
        gs[:, :nrows], 
        projection = ccrs.PlateCarree()
        )
    
    ax1 = fig.add_subplot(gs[0, nrows:])
    args = dict(sharey = ax1)
    
    ax2 = fig.add_subplot(gs[1, nrows:], **args)
    ax3 = fig.add_subplot(gs[2, nrows:], **args)
    ax4 = fig.add_subplot(gs[3, nrows:], **args)
    axes = [ax1, ax2, ax3, ax4]
    
    return fig, ax_map, axes

def plot_roti_timeseries(
        axes, 
        df, dn, 
        corners
        ):
    
    key = list(corners.keys())
    
    for i, ax in enumerate(axes):
        
        k = key[i]
        xlim, ylim = corners[k]
       
        
        sel = df.loc[
            (df.index < dn) & 
            (df.lon > xlim[0]) & 
            (df.lon < xlim[1]) & 
            (df.lat > ylim[0]) & 
            (df.lat < ylim[1])
            ]
        
        ax.text(
            0.03, 0.75,
            f'Box {i + 1}', 
            transform = ax.transAxes
            )
    
        ax.scatter(sel.index, sel.roti, 
                   s = 3, color = 'k')
        ax.set(
            yticks = np.arange(0, 4, 1),
            xlim = [df.index[0], df.index[-1]]
            )
        
        ax.tick_params(
            axis='y', 
            labelright = True, 
            labelleft = False, 
            right = True, 
            left = False)
        
        if i != -1:
            ax.set(xticklabels = [])
            
        # if i == 0:
        #     ax.legend(
        #         bbox_to_anchor = (.5, 1.5), 
        #         loc = "upper center", 
        #         ncol = 2,
        #         columnspacing = 0.7
        #         )
        
    b.format_time_axes(axes[-1])



 
def plot_roti_tec_variation(df, start, dn, twilight = 12):
    
    
    fig, ax_map, axes = multi_layout(nrows = 4)
    
    corners = pl.plot_tec_map(dn, ax = ax_map)
    
    term_lon, term_lat = gg.terminator2(dn, 18)
    
    ax_map.scatter(term_lon, term_lat, s = 10)
    
    plot_roti_timeseries(axes, df, dn, corners)
    
    fig.text(0.93, 0.3, 
        "ROTI (TECU/min)", 
        rotation = "vertical", 
        fontsize = 25
        )
    
    return fig

def main():
    
    start = dt.datetime(2013, 12, 25, 21, 29)
    
    df =  pb.concat_files(
        start, 
        root = 'D:\\'
        )
    
    df = b.sel_times(df, start)
            
    dn = range_time(start, 30)
 