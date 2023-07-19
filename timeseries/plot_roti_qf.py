import matplotlib.pyplot as plt
from common import plot_roti, plot_terminators
import pandas as pd
import settings as s
import datetime as dt

def plot_roti_QF():

    fig, ax = plt.subplots(
                figsize = (14, 8),
                sharex = True,
                nrows = 2,
                dpi = 300
                )
    
    plt.subplots_adjust(hspace = 0.1)
    
    cha = "database/Digisonde/SAA0K_20130316(075)_cha_raw"
    
    df = pd.read_csv(cha, index_col = 0)
    df.index = pd.to_datetime(df.index)
    ax[0].scatter(df.index, df["QF"], s = 35)
    
    ax[0].set(ylabel = "QF (km)", ylim = [0, 120], 
              title = 'São Luis')
    
    plot_roti(ax[1], df, hour_locator = 12, station = "salu")
    
    name = ['Digissonda', 'Receptor']
    for i, ax in enumerate(ax.flat):
        plot_terminators(ax, df)
        
        letter = s.chars()[i]
        ax.text(0.02, 0.82, f"({letter}) {name[i]}", 
                transform = ax.transAxes)
        
        ax.axvspan(dt.datetime(2013, 3, 17, 21), 
                   dt.datetime(2013, 3, 18, 5),
                   alpha = 0.5, color = "gray", 
                   label = 'Sem EPBs')
        if i == 0:
            ax.legend(loc = 'upper right')
            
    s.config_labels(fontsize = 20)
    
    fig.savefig("results/figures/QF_roti.png", dpi = 300)
    
