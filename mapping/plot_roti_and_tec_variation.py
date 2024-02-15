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
    
    fig = plt.figure(dpi = 300, figsize = (19, 8))
    
    gs = GridSpec(nrows, 8)
    
    plt.subplots_adjust(wspace = 3, hspace = 0.1)
    
    ax_map = fig.add_subplot(
        gs[:, :nrows], 
        projection = ccrs.PlateCarree()
        )
    

    axes = []
    for row in range(4):
    
        axes.append(fig.add_subplot(gs[row, nrows:]))
        
    return fig, ax_map, axes


def plot_roti_tec_variation(df, start, dn, vmax = 10):
    
    fig, ax_map, axes = multi_layout(nrows = 4)
    
    pl.plot_tec_map(dn, ax = ax_map, vmax = vmax)
    
    local_terminator = gg.first_edge(year = dn.year)
    
    pl.plot_roti_timeseries(
        axes, 
        df, 
        dn, 
        start,  
        local_terminator,
        right_ticks = True
        )

    fig.text(
        0.93, 0.3, "ROTI (TECU/min)", 
        rotation = "vertical", 
        fontsize = 25
        )
    
    return fig

def main():
    
    start = dt.datetime(2022, 7, 25, 0)
    
    df =  pb.concat_files(
        start, 
        root = 'D:\\'
        )
    
    df = b.sel_times(df, start, hours = 8)
  
    dn = range_time(start, 450)
    
    plot_roti_tec_variation(df, start, dn)
 
    
    
main()