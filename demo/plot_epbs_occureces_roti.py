import pandas as pd
import datetime as dt
import base as b 
import matplotlib.pyplot as plt
import PlasmaBubbles as pb 


year = 2018
infile = f'database/EPBs/longs/{year}.txt'
dn = dt.datetime(year, 1, 4, 20)
df = b.load(infile)

ds = b.sel_times(df, dn, hours = 10)

def plot_epbs_occurrences_roti(ds):
    

    fig, ax = plt.subplots(
        nrows = 2, 
        sharex = True, 
        figsize = (12, 6)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    delta = 3
    ax[0].plot(ds)
    
    ax[0].set(ylim = [0, 5], 
              ylabel = 'ROTI (TECU/min)')
    ax[0].axhline(1, lw = 1)
    
    ax[0].legend(
        ds.columns, 
        ncol = 5, title = 'zones',
        bbox_to_anchor = (.5, 1.7), 
        loc = "upper center")
    
    ax[1].plot(pb.get_events(ds, delta_rng = delta))
    
    ax[1].set(ylabel = 'EPBs occurence')
    
    ax[1].text(0.03, 0.8, f'$\\Delta t$ = {delta} min', 
               transform = ax[1].transAxes)
    
    b.format_time_axes(ax[1])