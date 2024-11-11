import matplotlib.pyplot as plt
import base as b
import PlasmaBubbles as pb
from math import ceil 
import core as c
import pandas as pd 

def join_data():
    df = b.load('events_class2')
    df = df.loc[df.index.year < 2023]
    ds = pb.sel_typing(df, typing = 'midnight')
    ds1 = c.count_occurences(ds).year
    # df = df[[-50, -60, -70]]
      
    df = c.geo_index()
    
    df = df.resample('1Y').mean()
    
    # print(df)
    
    df.index = df.index.year 
    
    return pd.concat([df, ds1], axis = 1)
def plot_month(
        ax, 
        x, y
        ,
        norm = True
        ):
    

    ax.scatter(x, y, s = 30)
    
    fit = b.linear_fit(x, y)
    
    intercept = round(fit.intercept, 2)
    slope = round(fit.slope[0], 2)
    r2 = str(fit.r2_score)
    
    ax.plot(x, fit.y_pred, 
            lw = 2, color = 'r')
    
    info = '$R^2 = $' + f'{r2}'
    ax.text(
        0.2, 0.8, 
        info, 
        transform = ax.transAxes
        )
    
    return ax


def plot_roti_vs_solar_flux(
        flux = 'f107a',
        roti = 'mean', 
        lon = -40,
        norm = True
        ):

    
    ds = join_data().dropna()
    
    sectors = [-50, -60, -70]
        
    fig, ax = plt.subplots(
        dpi = 300, 
        sharex = True, 
        sharey = True,  
        ncols = len(sectors), 
        figsize = (14, 6)
        )
    
    plt.subplots_adjust(wspace = 0.1)
    
    for i, sector in enumerate(sectors):
        
        x = ds['f107a'].values
        y = ds[sector].values
        

        plot_month(
            ax[i], 
            x, y, 
            norm = norm
            )
        
        ax[i].set(title = f'Sector: {sector}')
        
        # name = ds1.index[0].strftime('%B')
        # ax.set(title = name)
        

    return fig

# fig = plot_roti_vs_solar_flux()

df = c.geo_index()
  
df = df.resample('1M').mean()

df['month'] = df.index.month
df['year'] = df.index.year

ds = pd.pivot_table(
    df, 
    columns = 'year', 
    index = 'month', 
    values = 'kp'
    ) 

ds.mean(axis = 1).plot()
