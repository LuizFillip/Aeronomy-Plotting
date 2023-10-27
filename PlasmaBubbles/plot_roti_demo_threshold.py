import PlasmaBubbles as pb 
import matplotlib.pyplot as plt 
import base as b
import GNSS as gs 
import os 
from scipy.stats import weibull_min
import numpy as np

PATH_LIMIT = 'database/epbs/night_day.txt'

b.config_labels()
     
def plot_weibull(ax, day):
    
    data = day['roti'].values
    
    std = data.std()
    avg = data.mean()
    
    ax.axvline(
        avg + 4 * std, lw = 2,
        color = 'r', 
        label = '$\mu + 4 \sigma$')
    ax.axvline(
        avg, lw = 2, 
        color = 'b', label = '$\mu$')


    shape, loc, scale = weibull_min.fit(data)
    
    weibull_dist = weibull_min(
        shape, loc=loc, scale=scale)
    
   
    x = np.linspace(min(data), max(data), 50)
    
    fitted_pdf = weibull_dist.pdf(x) 
    
    ax.hist(data, bins = x, 
            density = True, 
            color = 'gray', 
            alpha = 0.3,
            edgecolor = 'black'
            )
    
    ax.plot(
        x, 
        fitted_pdf, 
        label = 'Weibull Fit', 
        lw = 3
        )
    
    vmin, vmax = min(data), max(data)

    
    ax.set(
        ylabel = 'Probability density', 
        xlabel = 'ROTI (TECU/min)',
        ylim = [0, 22],
        xlim = [-0.05, 0.3],
        xticks = np.arange(vmin, vmax, 0.1)
        )
    
    ax.legend( 
        ncol = 3, 
        loc = 'upper center', 
        bbox_to_anchor = (-.1, 1.15)
        )
    
    
args = dict(
     marker = 'o', 
     markersize = 3,
     linestyle = 'none', 
     color = 'gray', 
     alpha = 0.3, 
     )
    

def plot_data_roti(ax, df):
    
    df = df['roti']
    
    ax.plot(df, **args)
    
    std = df.std()
    avg = df.mean()
    
    ax.axhline(
        avg + 4 * std, 
        color = 'r', 
        lw = 2, 
        label = '$\mu + 4 \sigma$'
        )
    
    ax.axhline(
        avg, 
        color = 'b', 
        lw = 2, 
        label = '$\mu$'
        )
    
    ax.set(
        xlim = [df.index[0], df.index[-1]],
        ylim = [0, 1],
        ylabel = 'ROTI (TECU/min)'
        )
    
    b.format_time_axes(ax)
    
    # ax.legend()
    


def plot_roti_demo_threshold(ds):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        ncols = 2,
        figsize = (12, 6)
        )
    
    plt.subplots_adjust(wspace = 0.3)
    
    plot_data_roti(ax[0], day)
    
    plot_weibull(ax[1], day)
    
    names = ['Daytime ROTI', 
             'ROTI Distribution']
    
    for i, ax in enumerate(ax.flat):
        l = b.chars()[i]
        n = names[i]
        ax.text(
            0.05, 0.9, f'({l}) {n}', 
            transform = ax.transAxes
            )
    
    return fig

path = gs.paths(2013, 76, root = os.getcwd())

df = pb.load_filter(path.fn_roti)

receivers = [
    'pepe',
     'mabb',
     'mabs',
     'crat',
     'topl',
     'maba',
     'pitn',
     'picr',
     'brft',
     'ceft',
     'ceeu',
     'salu',
     'impz'
     ]
    

ds = df.loc[df['sts'].isin(receivers)]

day = ds.between_time(
    '12:00', '20:00'
    )

fig = plot_roti_demo_threshold(day)


# fig.savefig(b.LATEX('daytime_distribution'), dpi = 400)