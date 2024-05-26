import base as b
import pandas as pd
import digisonde as dg 
import matplotlib.pyplot as plt 
import numpy as np 


PATH_IONO = 'digisonde/data/chars/'

def average(ax, infile):
    
    df = dg.chars(PATH_IONO + infile)
    
    df = df.between_time('20:00', '08:00')
    
    df['time'] = b.time2float(df.index, sum_from = 18)
    
    df['day'] = df.index.day 
    df['hF2'] = b.smooth2(df['hF2'], 3)
    ds = pd.pivot_table(
        df,
        values = 'hF2',
        columns = 'day',
        index = 'time'
        ) 
    
    avg = ds.mean(axis = 1)
 
    std = ds.std(axis = 1)
    
    ax.errorbar(
        avg.index, 
        avg, 
        yerr = std, 
        linestyle = 'none',
        marker = 'o',
        capsize= 5, color = 'k', lw = 2 )

def day_target(ax, infile):

    df = dg.chars(PATH_IONO + infile)
    dn = df.index[0].strftime('%d %B %Y')
    df.index = b.time2float(df.index, sum_from = 18)
    df['hF2'] = b.smooth2(df['hF2'], 3)
    
    ax.plot(
        df['hF2'], 
        lw = 2,
        color= 'red', 
        label = dn
        )
    
    ax.set(
        xlim = [21, 31], 
        ylim = [100, 500],  
        yticks = np.arange(100, 600, 100),
        xticks = np.arange(21, 32, 1),
        ylabel = 'h`F2 (km)', 
        title = dg.embrace_infos[infile[:5]]
        )
    
    ax.legend(loc = 'upper left')

def plot_hF2_monthly_and_target():
    
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (12, 10), 
        nrows = 2,
        sharey = True, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.2)
    
    average(ax[0], 'SAA0K_20220701(182).TXT')
    
    day_target(ax[0], 'SAA0K_20220724(205).TXT')
    
    average(ax[1], 'CAJ2M_20220701(182).TXT')
    
    day_target(ax[1], 'CAJ2M_20220724(205).TXT')
    
    ax[1].set(xlabel = 'Universal time')

    return fig 



fig = plot_hF2_monthly_and_target()

