import matplotlib.pyplot as plt
import base as b 
import datetime as dt 
import numpy as np


b.config_labels()

lbs = b.labels

args_scatter = dict(s = 30, alpha = 0.4, color = 'gray')


def plot_gamma(ax, df):
    
    df = df * 1e3
    
    ax.scatter(df.index, df, **args_scatter)
    
    avg = b.smooth2(df, 27)
    ax.plot(df.index, avg, lw = 2)
    
    ax.set(
        ylim = [0, 4], 
        yticks = np.arange(0, 5, 1),
        ylabel = b.y_label('gamma'),
        xlim = [df.index[0], df.index[-1]]
        )

    return df


def plot_grad(ax, df):
    
    df = df * 1e5

    ax.scatter(df.index, df, **args_scatter)
    
    ax.plot(df.index, b.smooth2(df, 27), lw = 2)

    ax.set(
        ylim = [0, 5], 
        yticks = np.arange(0, 6, 1),
        ylabel = b.y_label('K')
        )
    

    
def plot_ratio(ax, df):
    
    ax.scatter(df.index, df, **args_scatter)

    
    ax.plot(df.index, b.smooth2(df, 27), lw = 2)
    
    ax.axhline(1, linestyle = '--')
    
    vmin, vmax, step = 0.9, 1, 0.05
    ax.set(
        ylim = [vmin, vmax], 
        yticks = np.arange(vmin, vmax + step, step),
        ylabel = b.y_label('ratio')
        )
    
def plot_gravity(ax, df):
    
    ax.scatter(df.index, df, **args_scatter)
    
    ax.plot(df.index, b.smooth2(df, 27), lw = 2)
    
    ax.set(
        ylim = [0, 30], 
        ylabel = b.y_label('g_nui_eff')
        )
     

def plot_vzp(ax, df):
    
    ax.scatter(df.index, df, **args_scatter)
    
    ax.plot(df.index, b.smooth2(df, 27), lw = 2)
    
    ax.set(
        ylim = [0, 90], 
        yticks = np.arange(0, 100, 20),
        ylabel = b.y_label('vp')
        )
    return None 
    
def plot_wind(ax, df, limit = 10, step = 5):
    
    ax.scatter(df.index, df, **args_scatter)
    
    ax.plot(df.index, b.smooth2(df, 27), lw = 2)
    
    
    ax.set(
        ylim = [-limit, limit], 
        yticks = np.arange(-limit, limit + step, step),
        ylabel = b.y_label('UL')
        )
    
    
    ax.axhline(0, linestyle = '--')


def plot_annual_GRT(df, translate = False):

    fig, ax = plt.subplots(
        sharex = True,
        dpi = 300, 
        nrows = 6, 
        figsize = (12, 18), 
        )
    
    plt.subplots_adjust(hspace = 0.1)
     
    plot_ratio(ax[0], df['ratio'])
    plot_vzp(ax[1], df['vp'])
    plot_wind(ax[2], df['mer_perp'])
    plot_grad(ax[3], df['K'])
    
    plot_gravity(ax[4], df['ge'] / df['nui'])
    
    plot_gamma(ax[5], df['gamma'])

    b.plot_letters(ax, y = 0.8, x = 0.02, 
                   fontsize = 25)
    if translate:
        ax[5].set(xlabel = 'Years')
    else:
        ax[5].set(xlabel = 'Anos')
    return fig


def main():
    PATH_GAMMA = 'database/gamma/p1_saa.txt'
    
    df = b.load(PATH_GAMMA)

    df = df.loc[(df.index.time == dt.time(22, 0)) & 
                (df.index.year < 2023)]
    
    fig = plot_annual_GRT(df)
    
    FigureName = 'annual_grt_parameters'
    
    fig.savefig(b.LATEX(
        FigureName, 
        folder = 'paper2'), dpi = 400)



main()

# plt.show()
