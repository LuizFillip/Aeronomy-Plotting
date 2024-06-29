import numpy as np 
import base as b 
import core as c 
import pandas as pd 
import matplotlib.pyplot as plt 
import os

site = 'jic'


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

def plot_PRE_monthly():

    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (14, 6)
        )
    
    names = ['São Luís', 'Jicamarca']
    
    for i, site in enumerate(['saa', 'jic']):
        ds = set_data(site)
        
        ax.errorbar(
            ds.index, 
            ds.mean(axis = 1),
            yerr = ds.std(axis = 1),
            marker = 's',
            capsize = 5,
            lw = 2, 
            label = names[i]
            )
    ax.legend(loc = 'upper center', ncol = 2)
    
    
    ax.set(
           ylim = [0, 50],
           xlabel = 'Meses', 
           ylabel = 'Deriva vertical (m/s)',
           xticks = np.arange(1, 13, 1),
           xticklabels = b.month_names(
               sort = True, language = 'pt'),
           
           )
    
    return fig
    
    
# fig = plot_PRE_monthly()

# FigureName = 'seasonal_pre_sites'
  
# fig.savefig(
#       b.LATEX(FigureName, folder = 'climatology'),
#       dpi = 400
#       )