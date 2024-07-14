import numpy as np 
import base as b 
import core as c 
import pandas as pd 
import matplotlib.pyplot as plt 
import os

site = 'jic'

b.config_labels()


def set_data(site):
    years = '2013_2021.txt'
        
    PATH_PRE = 'digisonde/data/PRE/'
    
    path = os.path.join(
        PATH_PRE,
        site, 
        years
        )    
    df = b.load(path)
    df = df.rename(columns = {'vz':'vp'})
    df = df.loc[:, ['vp']]
    df = df.resample('1M').mean()
    df['year'] = df.index.year
    df['month'] = df.index.month
    
    return pd.pivot_table(
        df, 
        values = 'vp', 
        columns = 'year', 
        index = 'month'
        )



def plot_declination_difference(ax):
    
    ax_new = ax.twinx().twiny()
    
    doy = np.arange(1, 366, 1)

    
    for dec_site in [-20.9123, -1.193]:
   
        ax_new.plot(
            doy, 
            dec_site - b.declination(doy), 
            lw = 2, 
            linestyle = '--')
        
    
    ax_new.set(
        ylim = [-50, 50],
        xticklabels = [], 
        ylabel = 'Grau de alinhamento'
        )
    
    
    ax_new.axhline(0, lw = 2, linestyle = ':')
    
    return ax_new
def plot_PRE_monthly():

    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (16, 8)
        )
    
    names = ['São Luís', 'Jicamarca']
    marker = ['s', 'o']
    for i, site in enumerate(['saa', 'jic']):
        ds = set_data(site)
        
        ax.errorbar(
            ds.index, 
            ds.mean(axis = 1),
            yerr = ds.std(axis = 1),
            marker = marker[i],
            markersize = 20,
            fillstyle = 'none',
            capsize = 7,
            lw = 2, 
            label = names[i]
            )
    ax.legend(
        bbox_to_anchor = (0.5, 1.2),
        loc = 'upper center',
        ncol = 3)
    
    ax_new = plot_declination_difference(ax)
    ax.set(
           ylim = [0, 50],
           xlabel = 'Meses', 
           ylabel = 'Deriva vertical (m/s)',
           xticks = np.arange(1, 13, 1),
           xticklabels = b.month_names(
               sort = True, language = 'pt'),
           
           )
    fig.text(
        0.97, 0.23, 'Grau de alinhamento (°)', 
        rotation = 'vertical')
    return fig
    
    
fig = plot_PRE_monthly()

FigureName = 'seasonal_pre_sites'
  
fig.savefig(
      b.LATEX(FigureName, folder = 'climatology'),
      dpi = 400
      )

# ds = set_data(site)

# ds

