import matplotlib.pyplot as plt
import pandas as pd
import settings as s
import numpy as np
import digisonde as dg
from labels import Labels

    
def plot_contourf(
        ax, 
        df, 
        parameter = 'ne'
        ):
    
    ds = pd.pivot_table(
        df, 
        index = "alt", 
        values = parameter, 
        columns = df.index
        ).interpolate()
    
    
    img = ax.contourf(
        ds.columns, 
        ds.index, 
        ds.values, 
        30, 
        cmap = "rainbow")
    
    ticks = np.linspace(np.nanmin(ds.values), 
                        np.nanmax(ds.values), 4)
    
    lbs = Labels().infos[parameter]

    name = lbs['name']
    units = lbs['units']
    s.colorbar_setting(
            img, ax, ticks, 
            label = f'{name} ({units})'
            )
    
    ax.set(ylabel = "Altura (km)", 
           ylim = [150, 600])
    
    return ax


def plot_profilogram(df):
    
    fig, ax = plt.subplots(
            dpi = 300,
            sharex = True,
            sharey = True,
            nrows = 3,
            figsize = (12, 14)
    )
    
    
    plt.subplots_adjust(hspace = 0.1)
    
    s.config_labels(fontsize = 20)
    
    plot_contourf(ax[0], df, parameter = 'freq')
    plot_contourf(ax[1], df, parameter = 'ne')
    plot_contourf(ax[2], df, parameter = 'L')
    
    s.format_time_axes(
            ax[2], 
            hour_locator = 12, 
            day_locator = 1, 
            tz = "UTC",
            pad = 55
    )
    
    ax[0].set(title = "São Luis")
    
    return fig
    

def main():
    infile = "database/Digisonde/SAA0K_20130319(078)_pro"
    df = dg.load_profilogram(infile)
    
    df['L'] = df['L'] *1e5
    
    df = df.loc[~((df['L'] < -48) & 
                  (df['L'] > 300) &
                  (df['alt'] <= 150))]
      
    fig = plot_profilogram(df)
    
    # fig.savefig("digisonde/src/figures/profilogram_saa.png", dpi = 300)
    


