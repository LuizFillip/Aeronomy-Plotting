import base as b
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 
import GEO as gg

b.config_labels(fontsize = 35)



df = pd.read_csv('conds', index_col = 0)

df['dn'] = pd.to_datetime(df['dn'])


def plot_height_time_conductivities():
    
    dn =  pd.to_datetime(df['dn'].values[0])
    
    fig, ax = plt.subplots(
        nrows = 3, 
        dpi = 300, 
        sharex = True, 
        sharey = True,
        figsize = (12, 14)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    cols = ['parl', 'hall', 'perd']
    
    lb = b.labels

    for i, col in enumerate(cols):
        
        ds = pd.pivot_table(
            df, 
            values = col, 
            index = df.index, 
            columns = 'dn')
     
        gg.plot_sunrise_sunset(ax[i], dn, site = 'saa')
        vls = np.log10(ds.values) 
        
    
        vls = vls - np.min(vls)
        img = ax[i].contourf(
            ds.columns, 
            ds.index, 
            vls, 
            30, 
            cmap = 'rainbow'
            )
        l = b.chars()[i]
        name = lb[col]['name']
        ax[i].text(
            0.02,
            0.83,
            f'({l}) {name}', 
            transform = ax[i].transAxes, 
            fontsize = 35
            )
        ticks = np.linspace(np.nanmin(vls), np.nanmax(vls), 4)
        
        b.colorbar(
            img, 
            ax[i], 
            ticks, 
            label = b.y_label(col), 
            anchor = (.05, 0., 1, 1)
            )
        
        ax[i].set(yticks = np.arange(100, 600, 100))
        
    b.format_time_axes(
        ax[-1],
        pad = 80,
        hour_locator = 2, translate = False)
    
    
    
    ax[1].set_ylabel('Altitude (km)', fontsize = 45)

    return fig 

def main():
    
    fig = plot_height_time_conductivities()
    
    FigureName = 'Conductivities'
    
    fig.savefig(
    b.LATEX(FigureName, 
            folder = 'Iono'),
    dpi = 400
    )
    
