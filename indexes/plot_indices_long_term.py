import matplotlib.pyplot as plt
import base as b
import datetime as dt
import numpy as np

PATH_INDEX =  'database/indices/omni_pro.txt'


def plot_dst(ax, dst, limit = -100 ):
    
    ax.plot(dst)
    
    ax.set(
        xlim = [dst.index[0], dst.index[-1]], 
        ylim = [-300, 100],
        yticks = np.arange(-200, 100, 100),
        ylabel = "Dst (nT)"
        )
    
    # for limit in [-50, -100]:
    ax.axhline(limit, lw = 2, color = 'r')
    
    
    return dst

def plot_f107(ax, f107, limit = 86):
    
    ax.plot(f107)
    # ax.plot(
    #     f107a, 
    #     lw = 3, 
    #     color = 'cornflowerblue'
    #     )
        
    ax.set(
        ylabel = '$F_{10.7}$ (sfu)', 
        ylim = [50, 250],
        yticks = np.arange(50, 250, 50)
        )

    # for limit in [75, 110]:
    ax.axhline(
        limit, 
        lw = 2, 
        color = 'r'
        )
        
        
def plot_kp(ax, kp, me = 30):
    
    args = dict(alpha = 0.3)
    
    ax.bar(kp.index, kp, **args)
    
    mean = kp.resample(f'{me}D').mean()
    
    ax.bar(mean.index, mean, 
           color = 'k', 
           width = 10, 
           label = f'{me} days average')
    
    ax.set(
        ylabel = 'Kp', 
        ylim = [0, 10], 
        yticks = np.arange(0, 10, 2)
        )
    
    ax.axhline(3, lw = 2, color = 'r')
    
    ax.legend()
     

def plot_long_term(s_year, e_year):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (12, 10), 
        nrows = 3, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    df = b.load(PATH_INDEX)
    
    df["f107a"] = df["f107"].rolling(window = 5).mean(center = True)
    
    df = b.sel_dates(
        df, 
        dt.datetime(s_year, 12, 1), 
        dt.datetime(e_year, 1, 13)
        )
        
    plot_kp(ax[0], df['kp'])
    plot_dst(ax[1], df['dst'])
    plot_f107(ax[2], df['f107'])
  
    ax[2].set( 
        xlabel = 'years',
        xlim = [df.index[0], df.index[-1]]
        )
        
    c = b.chars()

    for i, ax in enumerate(ax.flat):
        
        ax.text(
            0.02, 0.85, f'({c[i]})', 
            transform = ax.transAxes
            )
        
    return fig
    


fig = plot_long_term(2012, 2023)

# FigureName = 'geomagnetic_indexes'

# fig.savefig(
#     b.LATEX(FigureName, folder = 'timeseries'),
#     dpi = 400
#     )