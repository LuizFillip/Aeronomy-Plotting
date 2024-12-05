import matplotlib.pyplot as plt
import base as b 
import datetime as dt 
import numpy as np
from matplotlib.ticker import AutoMinorLocator 
import GEO as gg 

b.config_labels(fontsize = 30)

lbs = b.labels

args_scatter = dict(s = 30, alpha = 0.4, color = 'gray')


def plot_gamma(ax, df, gamma, avg_run = 27):
    
    df[gamma] = df[gamma] * 1e3
    
    df['avg'] = df[gamma].rolling(f'{avg_run}D').mean()
    
    # df.index = df.index.map(gg.year_fraction)
    
    ax.scatter(df.index, df[gamma], **args_scatter)

    ax.plot(df['avg'], lw = 2)
        
    if gamma == 'gamma':
        ylim = [0, 4]
        step = 1
    else:
        ylim = [-0.02, 1]
        step = 0.4
        
    ax.set(
        ylim = ylim, 
        yticks = np.arange(0, ylim[1] + step, step),
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
        yticks = np.arange(0, 50, 10),
        ylim = [-2, 42], 
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


def plot_annual_GRT(
        df, 
        translate = False, 
        gamma = 'gamma'):
    
    if gamma == 'gamma':
        nrows = 6
    else:
        nrows = 5

    fig, ax = plt.subplots(
        sharex = True,
        dpi = 300, 
        nrows = nrows, 
        figsize = (16, 20), 
        )
    
    plt.subplots_adjust(hspace = 0.1)
     
    if gamma == 'gamma':
        plot_ratio(ax[0], df['ratio'])
        plot_vzp(ax[1], df['vp'])
        plot_wind(ax[2], df['mer_perp'])
        plot_grad(ax[3], df['K'])
        plot_gravity(ax[4], df['gr'])
        plot_gamma(ax[5], df, gamma)
    else:
        plot_ratio(ax[0], df['ratio'])
        plot_wind(ax[1], df['mer_perp'])
        plot_grad(ax[2], df['K'])
        plot_gravity(ax[3], df['gr'])
        plot_gamma(ax[4], df, gamma)
        

    b.plot_letters(ax, 
        y = 0.8, 
        x = 0.02, 
        fontsize = 35)
    
    if translate:
        xlabel = 'Years'
    else:
        xlabel = 'Anos'
        
    delta = dt.timedelta(days = 30)
    
    ax[-1].set(
        xlim = [df.index[0] - delta, 
                df.index[-1] + delta], 
        xlabel = xlabel)
    
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(n = 11))
    # plt.gca().xaxis.set_major_locator(AutoMinorLocator(n=1))
    
    fig.align_ylabels()
    return fig


def main():
    
    PATH_GAMMA = 'database/gamma/p1_saa.txt'
    
    df = b.load(PATH_GAMMA)
    
    gamma = 'gamma2'
    
    if gamma == 'gamma':
        time = dt.time(22, 0)
    else:
        time = dt.time(3, 0)

    df = df.loc[(df.index.time == time) & (df.index.year < 2023)] 
    
    df['gr'] = df['ge'] / df['nui']
    
    df['gamma2'] = df['ratio'] * df['K'] * (
        - df['mer_perp'] + df['gr'])
    
        
    fig = plot_annual_GRT(df, translate = False, gamma = gamma)
    
    FigureName = f'annual_{gamma}_parameters'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'climatology'), dpi = 300)



# main()

