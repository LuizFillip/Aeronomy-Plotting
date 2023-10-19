import matplotlib.pyplot as plt
import base as b
import os 


b.config_labels()   

PATH_PRE = 'digisonde/data/PRE/'

def set_data(site = 'saa'):

    infile = os.path.join(
        PATH_PRE, 
        f'{site}/2013_2021.txt'
        )
    
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
    yr = 2019
    df = df.loc[df.index.year == yr]
    # ax[0].axhline(df.mean().item())
    plot_pre_annual_site(ax[0], df)
    
    df = set_data(site = 'jic')
    
    df = df.loc[df.index.year == yr]
    # ax[1].axhline(df.mean().item())
    plot_pre_annual_site(ax[1], df)
    

    
    ax[1].set(xlabel = 'years')
    
    
plot_pre_annual()

# import numpy as np 
# from scipy.optimize import curve_fit


# df = set_data(site = 'jic')
# df = df.loc[df.index.year == 2015]
# # df = df.loc[~((df['vz'] > 30) | 
# #               (df['vz'] < 0))]





# N = 20
# df['avg'] = b.running(df['vz'], N)

# fig, ax = plt.subplots()

# ax.scatter(df.index, df['vz'])
# ax.plot(df['avg'], color = 'r')

# ax.set(ylim  = [-10, 50])