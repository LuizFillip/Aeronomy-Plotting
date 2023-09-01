import base as b 
import matplotlib.pyplot as plt
import datetime as dt
import PlasmaBubbles as pb 
import GNSS as gs
import os 
import pandas as pd

b.config_labels()




# fig.suptitle('04 de janeiro')

def dataset(year):
    
    dn = dt.datetime(year, 1, 1, 20)
    
    out = []
    for doy in range(1, 3):
        path = gs.paths(
            year, doy, root = os.getcwd()
            ).fn_roti
        
        out.append(pb.long_dataset(path))
        
    ds = pd.concat(out)
    
    ds = ds[ds < 5]
         
    df = b.sel_times(ds, dn)
    
    df.index = b.time2float(df.index)
    
    df['epb'] = df.max(axis = 1)
    return df






def concat_datasets(
        years):
    
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
        hspace = 0.2, 
        wspace = 0.1
        )

    cols = ds.columns
    for i, ax in enumerate(ax.flat):
     
        ax.plot(ds[cols[i]], 
                marker = 'o', 
                linestyle = 'none', 
                markersize = 4)
        
        ax.set(title = cols[i])
        
        ax.axhline(1, lw = 2)
        
    
        

plot_annual_compararion_roti(years)