import matplotlib.pyplot as plt
import base as b
import datetime as dt
import numpy as np
import GEO as gg

PATH_INDEX =  'database/indices/omni_pro2.txt'


def plot_dst(ax, dst, limit = -100 ):
    
    ax.plot(dst)
    
    ax.set(
        ylim = [-200, 50],
        yticks = [-30, -100, -150],
        ylabel = "Dst (nT)"
        )
    
    ax.axhline(0, lw = 1.5, linestyle = ':')
    ax.axhline(-30, lw = 2, color = 'r')
    ax.axhline(limit, lw = 2, color = 'r')

    return None

def plot_f107(
        ax, mean = None, float_index = True, 
              color = 'k'):
    
    
    df = b.load(PATH_INDEX)
        
    df["f107a"] = df["f107"].rolling(
        window = 5).mean(center = True)
    
    if float_index:
        df.index = df.index.map(gg.year_fraction)
        
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
        
        
def plot_kp(ax, df, mean = 30):
    
    args = dict(alpha = 0.3)
    
    ax.bar(df.index, df['kp'], **args)
    
    # ax1 = ax.twinx()
    
    # f107 = df['f107'].resample('1M').mean()
    
    # ax1.plot(f107, color = 'red')
    if mean is not None:
        mean = df['kp'].resample(f'{mean}D').mean()
        
        ax.bar(mean.index, mean, 
               color = 'k', 
               width = 10, 
               label = f'{mean} days average'
               )
    
    ax.set(
        ylabel = 'Kp', 
        ylim = [0, 9], 
        yticks = np.arange(0, 9, 2)
        )
    
    ax.axhline(3, lw = 2, color = 'r')
 
    return None

def plot_magnetic_fields(ax, ds):
    
    ax.plot(ds[['by', 'bz']], label = ['by', 'bz'] )
    
    ax.axhline(0, lw = 1, linestyle = '--', color = 'k')
    
    ax.set(
        ylim = [-10, 30], 
        ylabel = '$B_y/B_z$ (nT)'
        )
    
    ax.legend(
        loc = 'upper right', 
        ncol = 2
        )
    
    return None 


def plot_long_term(s_year, e_year):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (16, 12), 
        nrows = 3, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    df = b.load(PATH_INDEX)
        
    df["f107a"] = df["f107"].rolling(
        window = 5).mean(center = True)
    
    df = b.sel_dates(
        df, 
        dt.datetime(2023, 1, 1), 
        dt.datetime(2023, 12, 31)
        )
    
        
    plot_kp(ax[2], df, mean = None)
    plot_dst(ax[1], df['dst'])
    plot_magnetic_fields(ax[0], df)
    ax[-1].set(xlim= [df.index[0], df.index[-1]])
    
    b.format_month_axes(ax[-1], translate = False)
  
    b.plot_letters(ax, y = 0.83, x = 0.02, fontsize = 40)
        
    return fig
    

def main():
    fig = plot_long_term(2022, 2024)
    
    FigureName = 'geomagnetic_indexes_2023'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'indices'),
        dpi = 400
        )

# df = b.load(PATH_INDEX)

# df