import matplotlib.pyplot as plt
import base as b 
import os
import datetime as dt 
import events as ev 

PATH_GAMMA = 'database/Results/gamma/'

def plot_annual_variation(df, integrated = True):

    fig, ax = plt.subplots(
        sharex = True,
        dpi = 300, 
        nrows = 2, 
        figsize = (14, 8), 
        )
    
    plt.subplots_adjust(hspace = 0.5)
    

    
    # ax[0].legend(loc = 'upper center',
    #     bbox_to_anchor = (.5, 1.9),
    #     title = title, ncol = 2)
    # ax[1].legend(title = title, ncol = 2, 
    #              loc = 'upper center',
    #                  bbox_to_anchor = (.5, 1.5),)
        
    
    return fig

infile = 'FluxTube/data/reduced/jic/2015.txt'


fig, ax = plt.subplots(
    sharex = True,
    dpi = 300, 
    figsize = (14, 8), 
    )

site = 'jic'
path = os.path.join(
   PATH_GAMMA,
   f't_{site}.txt'
   )

df = b.load(path)
df = df.loc[df.index.year == 2019]

df['night'].plot(ax = ax)

site = 'saa'
path = os.path.join(
   PATH_GAMMA,
   f't_{site}.txt'
   )

df = b.load(path)
df = df.loc[df.index.year == 2019]

df['night'].plot(ax = ax)