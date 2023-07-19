import numpy as np
import matplotlib.pyplot as plt
import RayleighTaylor as rt
# import results as r
from events import storms_types
import settings as s



def plot_probability_distribution():
    fig, ax = plt.subplots(
        dpi = 300,
        nrows = 3, 
        sharex = True,
        sharey = True,
        figsize = (8, 4)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    infile ='database/Results/joined/vp_epbs.txt'
    years = [2013, 2014, 2015]
    for row, year in enumerate(years):
    
        ds = storms_types(infile, year = year)
        
        labels = ['quiets', 'modered', 'intense']
        events = [ds.quiets, ds.modered, ds.intense]
        
        f = plot_occurrence_in_periods(
            ax[row],
            events, 
            labels,
            col_gamma = 'vp',
            year = year
            )
    
    ax[0].legend(
                 bbox_to_anchor = (0.5, 1.3), 
                 ncol = 3, 
                 loc = 'upper center')
    ax[1].set(ylabel = 'EPBs occurrence probability (\%)')
    ax[2].set(xlabel =  '$V_{zp}$ (m/s)')
    
    
    s.add_lines_and_letters(
            ax, 
            names = years)