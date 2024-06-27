import PlasmaBubbles as pb 
import matplotlib.pyplot as plt 
import base as b
import GNSS as gs 
import os 
from scipy.stats import weibull_min
import numpy as np
from scipy.stats import norm

PATH_LIMIT = 'database/epbs/night_day.txt'

b.config_labels()

args = dict(
      marker = 'o', 
      markersize = 3,
     linestyle = 'none', 
     color = 'gray', 
     alpha = 0.3, 
     )
    
     
def plot_weibull(ax, day):
    
    data = day['roti'].values
    # print(data)
    std = data.std()
    avg = data.mean()
    threshold = avg + 4 * std
    
    ax.axvline(
        threshold, lw = 2,
        color = 'r', 
        label = '$\mu + 4 \sigma$'
        )
    ax.axvline(
        avg, lw = 2, 
        color = 'b', 
        label = '$\mu$'
        )
    
    
    shape, loc, scale = weibull_min.fit(data)
    
    weibull_dist = weibull_min(
        shape, loc=loc, scale=scale)
    
   
    x = np.linspace(min(data), max(data), 50)
    
    fitted_pdf = weibull_dist.pdf(x) 
    
    ax.hist(
        data, 
        bins = x, 
            density = False, 
            color = 'gray', 
            alpha = 0.3,
            edgecolor = 'black'
            )
    
    ax.plot(
        x, 
        fitted_pdf * 40, 
        label = 'Ajuste Weibull', 
        lw = 3
        )

    
    ax.set(
        ylabel = 'Frequência de ocorrência', 
        xlabel = 'ROTI (TECU/min)',
        ylim = [0, 1000]
        # xlim = [-0.05, 0.3],
        # xticks = np.arange(vmin, vmax, 0.2)
        )
    
    ax.legend( 
        ncol = 3, 
        loc = 'upper center', 
        bbox_to_anchor = (-.1, 1.15)
        )
    
    return ax
    
    


def plot_data_roti(ax, df):
    
    df = df['roti']
    
    ax.plot(df, **args)
    
    std = df.std()
    avg = df.mean()
    
    threshold = avg + 4 * std
    # print(threshold)
    ax.axhline(
        threshold, 
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
    
    b.format_time_axes(ax, translate = False)
    
    return ax
    


def plot_roti_demo_threshold(ds, translate = False):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        ncols = 2,
        figsize = (14, 8)
        )
    
    plt.subplots_adjust(wspace = 0.3)
    
    plot_data_roti(ax[0], ds)
    
    plot_weibull(ax[1], ds)
    
    if translate:
        names = ['Daytime ROTI', 'ROTI Distribution']
    else:
        names = ['ROTI diurno', 'Distribuição do ROTI']
    
    for i, ax in enumerate(ax.flat):
        l = b.chars()[i]
        n = names[i]
        ax.text(
            0.05, 0.9, f'({l}) {n}', 
            transform = ax.transAxes
            )
    
    return fig

def set_data():

    path = gs.paths(2013, 359, root = 'D:\\')
    
    df = pb.load_filter(path.fn_roti())
    
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
        
    
    df = df.loc[df['sts'].isin(receivers)]
    
    return df.between_time('12:00', '20:00' )


# ds = set_data()


# fig = plot_roti_demo_threshold(ds)

# fig.savefig(
#     b.LATEX('threshold_eval', folder = 'products'),
#     dpi = 400)
# plt.show()
