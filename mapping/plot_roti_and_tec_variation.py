import datetime as dt 
import plotting as pl
import base as b
import PlasmaBubbles as pb 

b.config_labels(fontsize = 25)

def range_time(start, mi):
        
    return start + dt.timedelta(minutes = mi)

def plot_roti_tec_variation(
        df, 
        start, 
        dn, 
        vmax = 100
        ):
    
    fig, ax_map, axes = b.multi_layout(nrows = 4)
    
    pl.plot_tec_map(dn, ax = ax_map, vmax = vmax)
        
    pl.plot_roti_timeseries(
        axes, 
        df, 
        dn, 
        start,  
        right_ticks = True
        )
    

    fig.text(
        0.93, 0.3, "ROTI (TECU/min)", 
        rotation = "vertical", 
        fontsize = 25
        )
    
    return fig

def main():
    
    start = dt.datetime(2014, 2, 9, 21)
    
    df =  pb.concat_files(
        start, 
        root = 'D:\\'
        )
    
    df = b.sel_times(df, start, hours = 8)
  
    dn = range_time(start, 200)
    
    fig = plot_roti_tec_variation(df, start, dn)
    
    
    
# main()