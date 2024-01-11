import cartopy.crs as ccrs
import GEO as gg
import matplotlib.pyplot as plt
import datetime as dt 
from matplotlib.gridspec import GridSpec
import plotting as pl
import base as b
import PlasmaBubbles as pb 

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


def plot_roti_tec_variation(df, start, dn, twilight = 12):
    
    
    fig, ax_map, axes = multi_layout(nrows = 4)
    
    corners = pl.plot_tec_map(dn, ax = ax_map)
    
    eq_lon, eq_lat = pl.plot_terminator_and_equator(
            ax_map, dn, twilight = 18)
    
    pl.plot_roti_timeseries(
        axes, 
        df, 
        dn, 
        corners, 
        right_ticks = True
        )
    
    local_term = pl.first_of_terminator(
            ax_map, 
            corners, 
            eq_lon, 
            eq_lat
            )
    # print(local_term)
    pl.plot_lines( 
            axes, 
            start,  
            local_term
            )
    
    fig.text(0.93, 0.3, "ROTI (TECU/min)", 
        rotation = "vertical", 
        fontsize = 25
        )
    
    return fig

def main():
    
    start = dt.datetime(2013, 12, 25, 20)
    
    df =  pb.concat_files(
        start, 
        root = 'D:\\'
        )
    
    df = b.sel_times(df, start)
            
    dn = range_time(start, 200)
 
    plot_roti_tec_variation(df, start, dn, twilight = 12)
    plt.show()
# main()