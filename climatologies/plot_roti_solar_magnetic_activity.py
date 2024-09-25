import matplotlib.pyplot as plt 
import base as b 
import plotting as pl 
import core as c 

df = b.load('all_maximus2')
df['mean'] = df.mean(axis = 1)

#%%%

PATH_INDEX =  'database/indices/omni_pro2.txt'
import numpy as np 

def plot_F107(
        ax, 
        mean = None, 
        float_index = True, 
        color = 'k'
        ):
    
    
    df = b.load(PATH_INDEX)
        
    df["f107a"] = df["f107"].rolling(
        window = 81).mean(center = True)
    
    # if float_index:
    #     df.index = df.index.map(gg.year_fraction)
        
    ax.plot(df['f107'], color = color)
    
    if mean is not None:
        ax.plot(
            df['f107a'], 
            lw = 3, 
            color = 'cornflowerblue'
            )
        
    ax.set(
        ylabel = '$F10,7$ (sfu)', 
        ylim = [50, 300],
        yticks = np.arange(50, 350, 100)
        )   
    return None
        

def plot_annual_roti_and_indices(df):
    
    fig, ax = plt.subplots(
        sharex = True,
        dpi = 300, 
        nrows = 2,
        figsize = (16, 10), 
        )

    plt.subplots_adjust(hspace = 0.1)
    
    ds = df.resample('1D').mean()

    idx = c.geo_index(
            cols = ['f107a', 'f107', 'kp', 'dst'],
            syear = 2013, 
            eyear = 2022
            )

    plot_F107(
        ax[0], 
        idx,
        )
    # pl.plot_Kp(ax[0], idx, kp_level = None)
    ax[-1].plot(ds['mean'])

    ax[-1].set(
        ylim = [0, 1.5], 
        xlim = [idx.index[0], idx.index[-1]], 
        xlabel = 'Anos', 
        ylabel = 'ROTI$_{max}$ (TECU/min)'
        )

    b.plot_letters(
        ax, y = 0.85, x = 0.02, 
        fontsize = 40
           )
    
    return fig
    
def main():
    fig = plot_annual_roti_and_indices(df)
    FigureName = 'annual_roti_and_indices'
    fig.savefig(
        b.LATEX(FigureName, folder = 'climatology')
        )
    
    
