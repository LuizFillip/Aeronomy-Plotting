import matplotlib.pyplot as plt
import pandas as pd
import base as b

b.config_labels()   

def set_data(site = 'saa'):

    infile = f'digisonde/data/PRE/{site}/2013_2021.txt'
    
    df = b.load(infile)
    
    df.rename(
        columns = {'vp': 'vz'}, 
        inplace = True
        )
    
    return df 

def plot_pre_annual_site(ax, df):
    
    
       
    ax.scatter(df.index, df['vz'])
    
    ax.set(
        ylabel = "Vertical drift (m/s)", 
        xlim = [df.index[0], df.index[-1]], 
        ylim = [-10, 80]
        )
    
    



def plot_pre_annual():
    
    fig, ax = plt.subplots(
        dpi = 300,
        nrows = 2,
        sharex = True,
        sharey = True,
        figsize = (14, 8)
        )
    
    df = set_data(site = 'saa')
    plot_pre_annual_site(ax[0], df)
    
    df = set_data(site = 'jic')
    plot_pre_annual_site(ax[1], df)
    
    
    ax[1].set(xlabel = 'years')