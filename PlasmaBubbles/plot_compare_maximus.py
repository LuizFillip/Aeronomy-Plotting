import PlasmaBubbles as pb
import matplotlib.pyplot as plt 
import numpy as np 
import base as b 
import datetime as dt 




def plot_compare_maximus(
        long = -60, 
        factor = 2
        ):

    fig, ax = plt.subplots(
        nrows = 3, 
        dpi = 300,
        sharey = True,
        sharex = True, 
        figsize = (12, 6)
        )
    
    
    dn = dt.datetime(2015, 2, 17, 21)
    
    
    df = b.sel_times(
        pb.concat_files(dn), dn, hours = 15
        )
    
    
    
    
    ax[0].plot(pb.raw_maximus(df, long))
    
    ax[1].plot(pb.raw_maximus(df, long, factor))
    
    ax[2].plot(pb.raw_maximus(
            pb.reducing_all_df(df, factor), long
            )
        )
    
    b.format_time_axes(ax[2])
    
    ax[0].set(ylim = [0, 4])
    
    
plot_compare_maximus()