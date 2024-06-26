import matplotlib.pyplot as plt
import base as b 
import datetime as dt 
import numpy as np
from matplotlib.ticker import AutoMinorLocator 


b.config_labels()

lbs = b.labels

args_scatter = dict(s = 30, alpha = 0.4, color = 'gray')


def plot_gamma(ax, df, avg_run = 27):
    
    df = df * 1e3
    
    ax.scatter(df.index, df, **args_scatter)
    
    df = df.to_frame()
    df['avg'] = df['gamma'].rolling(f'{avg_run}D').mean()

    ax.plot(df['avg'], lw = 2)
    
    ax.set(
        ylim = [-0.2, 4], 
        yticks = np.arange(0, 5, 1),
        ylabel = b.y_label('gamma')
        )

    return None


def plot_grad(ax, df, avg_run = 27):
    
    df = df * 1e5

    ax.scatter(df.index, df, **args_scatter)
    df = df.to_frame()
    df['avg'] = df['K'].rolling(f'{avg_run}D').mean()

    ax.plot(df['avg'], lw = 2)

    ax.set(
        ylim = [0, 5], 
        yticks = np.arange(0, 6, 1),
        ylabel = b.y_label('K')
        )
    
    return None
    

    
def plot_ratio(ax, df, avg_run = 27):
    
    ax.scatter(df.index, df, **args_scatter)
    
    df = df.to_frame()
    df['avg'] = df['ratio'].rolling(f'{avg_run}D').mean()

    ax.plot(df['avg'], lw = 2)
    
    ax.axhline(1, linestyle = '--')
    
    vmin, vmax, step = 0.9, 1, 0.05
    ax.set(
        ylim = [vmin, vmax], 
        yticks = np.arange(vmin, vmax + step, step),
        ylabel = b.y_label('ratio')
        )
    
    return None
    
def plot_gravity(ax, df, avg_run = 27):
    
    ax.scatter(df.index, df, **args_scatter)
    
    df = df.to_frame()
    df['avg'] = df['gr'].rolling(f'{avg_run}D').mean()

    ax.plot(df['avg'], lw = 2)
    
    ax.set(
        yticks = np.arange(0, 40, 10),
        ylim = [-2, 32], 
        ylabel = b.y_label('gr')
        )
    
    return None
     

def plot_vzp(ax, df, avg_run = 27):
    
    ax.scatter(df.index, df, **args_scatter)
    
    df = df.to_frame()
    df['avg'] = df['vp'].rolling(f'{avg_run}D').mean()

    ax.plot(df['avg'], lw = 2)
    ax.set(
        ylim = [-5, 90], 
        yticks = np.arange(0, 100, 20),
        ylabel = b.y_label('vp')
        )
    return None 
    
def plot_wind(ax, df, limit = 13, step = 5):
    
    ax.scatter(df.index, df, **args_scatter)
    
    ax.plot(df.index, b.smooth2(df, 27), lw = 2)
    
    
    ax.set(
        ylim = [-limit, limit], 
        yticks = np.arange(-limit + 1, limit + 4, step),
        ylabel = b.y_label('UL')
        )
    
    
    ax.axhline(0, linestyle = '--')
    return None 


def plot_annual_GRT(df, translate = False):

    fig, ax = plt.subplots(
        sharex = True,
        dpi = 300, 
        nrows = 6, 
        figsize = (14, 18), 
        )
    
    df['gr'] = df['ge'] / df['nui']
    
    plt.subplots_adjust(hspace = 0.1)
     
    plot_ratio(ax[0], df['ratio'])
    plot_vzp(ax[1], df['vp'])
    plot_wind(ax[2], df['mer_perp'])
    plot_grad(ax[3], df['K'])
    
    plot_gravity(ax[4], df['gr'])
    
    plot_gamma(ax[5], df['gamma'])

    b.plot_letters(
        ax, 
        y = 0.8, 
        x = 0.02, 
        fontsize = 25)
    if translate:
        xlabel = 'Years'
    else:
        xlabel = 'Anos'
        
    delta = dt.timedelta(days = 30)
    
    ax[-1].set(
        xlim = [df.index[0] - delta, 
                df.index[-1] + delta], 
        xlabel = xlabel)
    
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(n=11))
    # plt.gca().xaxis.set_major_locator(AutoMinorLocator(n=1))
    return fig


def main():
    PATH_GAMMA = 'database/gamma/p1_saa.txt'
    
    df = b.load(PATH_GAMMA)

    df = df.loc[
        (df.index.time == dt.time(22, 0)) & 
        (df.index.year < 2023)]
    
    fig = plot_annual_GRT(df, translate=True)
    
    FigureName = 'annual_grt_parameters'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'paper2'), dpi = 300)



main()


