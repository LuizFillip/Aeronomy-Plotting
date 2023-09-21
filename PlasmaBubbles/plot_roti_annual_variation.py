import base as b 
import matplotlib.pyplot as plt
import datetime as dt
import PlasmaBubbles as pb 
import GNSS as gs
import os 
import pandas as pd

b.config_labels()


def dataset(year):
    
    dn = dt.datetime(year, 1, 1, 20)
    
    out = []
    for doy in range(1, 3):
        path = gs.paths(
            year, doy, root = os.getcwd()
            ).fn_roti
        
        out.append(pb.long_dataset(path))
        
    ds = pd.concat(out)
             
    df = b.sel_times(ds, dn)
    
    df.index = b.time2float(df.index)
    
    df['epb'] = df.max(axis = 1)
    return df



def concat_datasets(years):
    
    out = []
    for year in years: 
        out.append(dataset(year)['epb'])
        
    ds = pd.concat(out, axis=1)
    ds.columns = years
        
    return ds

years = list(range(2013, 2022))

# ds = concat_datasets(years)
    
# ds.to_csv('0101.txt')


def plot_annual_compararion_roti(years):
    
    
    ds = pd.read_csv('0101.txt', index_col = 0)

    fig, ax = plt.subplots(
        dpi = 300,
        ncols = 3, 
        nrows = 3,
        sharey = True,
        sharex = True,
        figsize = (18, 12)
        )


    plt.subplots_adjust(
        hspace = 0.15, 
        wspace = 0.05
        )

    cols = ds.columns
    
    df = b.load('database/indices/indeces.txt')
    df = df.interpolate()
    
    for i, ax in enumerate(ax.flat):
        
        year = cols[i]
        dn = dt.datetime(int(year), 1, 1)
        flux = df.loc[df.index == dn, 'f107a'].item()
        flux = round(flux, 3)
        
        ax.plot(
            ds[year], 
            marker = 'o', 
            linestyle = 'none', 
            markersize = 4
            )
        
        ax.text(
            0.1, 0.8, 
            f'F10.7 = {flux} sfu', 
            transform = ax.transAxes
            )
        
        ax.set(title = cols[i], ylim = [0, 5], 
               yticks = range(6))
        color = ['r', 'm']
        for i, threshold in enumerate([0.5, 1]):
            ax.axhline(
                threshold, 
                lw = 2, 
                color= color[i],
                label = f'{threshold} TECU/min'
                )
    
    ax.legend(title = 'Thresholds', 
              ncol = 2, 
              bbox_to_anchor = (-.5, 4),
              loc = "upper center")
    
    fontsize = 30   
        
    fig.text(
        0.08, 0.37, "ROTI (TECU/min)",
        rotation = "vertical", 
        fontsize = fontsize)
    
    fig.text(
        0.45, 0.05, "Universal time", 
        rotation = "horizontal", 
        fontsize = fontsize
        )
    
    fig.suptitle("1 de Janeiro", 
                 fontsize = fontsize, 
                 y = 0.95)
        
    
        

plot_annual_compararion_roti(years)


# ds = pd.read_csv('0101.txt', index_col = 0)


# year = 2013
