import PlasmaBubbles as pb
import matplotlib.pyplot as plt 
import numpy as np 
import base as b 
import datetime as dt 


b.config_labels()

def plot_compare_maximus(
        dn,
        long = -60, 
        factor = 3
        ):

    fig, ax = plt.subplots(
        nrows = 3, 
        dpi = 300,
        sharey = True,
        sharex = True, 
        figsize = (12, 6)
        )
    
    df = b.sel_times(
            pb.concat_files(dn), 
            dn, hours = 15
        )
    
    ax[0].plot(pb.raw_maximus(df, long))
    
    ax[1].plot(pb.raw_maximus(df, long, factor))
    
    ax[2].plot(
        pb.raw_maximus(
            pb.reducing_all_df(df, factor), long
            )
        )
    
    b.format_time_axes(ax[2])
    
    ax[0].set(ylim = [0, 4])
    
# dn = dt.datetime(2013, 3, 17, 21)
# plot_compare_maximus(dn, long = -40)