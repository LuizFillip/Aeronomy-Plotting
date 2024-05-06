import matplotlib.pyplot as plt
import base as b 
import datetime as dt 
import numpy as np


b.config_labels()

lbs = b.labels


def plot_gamma(ax, df):
    
    df = df * 1e3
    
    ax.scatter(
        df.index, df, 
        s = 30,
        alpha = 0.4, 
        color = 'gray'
        )
    
    avg = b.smooth2(df, 20)
    ax.plot(
        df.index, 
        avg, 
        lw = 2
        )
    
    ax.set(
        ylim = [0, 4], 
        yticks = np.arange(0, 5, 1),
        ylabel = b.y_label('gamma'),
        xlabel = 'Anos',
        xlim = [df.index[0], df.index[-1]]
        )
    
    ax.axhline(avg.max(), linestyle = '--')
    ax.axhline(avg.min(), linestyle = '--')
    
    return df


def plot_grad(ax, df):
    
    df = df * 1e5

    ax.plot(df, lw = 2)

    ax.set(
    
        ylim = [0, 5], 
        yticks = np.arange(0, 6, 1),
        ylabel = b.y_label('K')
        )
    

    
def plot_ratio(ax, df):
    
    ax.plot(df, lw = 2)
    
    ax.axhline(1, linestyle = '--')
    
    vmin, vmax, step = 0.8, 1.2, 0.1
    ax.set(
        ylim = [vmin, vmax], 
        yticks = np.arange(vmin, vmax + step, step),
        ylabel = b.y_label('ratio')
        )
    
def plot_gravity(ax, df):
    
    ax.scatter(df.index, df, s = 30, alpha = 0.4, color = 'gray')
    
    ax.plot(
        df.index, 
        b.smooth2(df, 20), 
        lw = 2
        )
    
    ax.set(
        ylim = [0, 30], 
        ylabel = b.y_label('g_nui_eff')
        )
     
    
def plot_vzp(ax, df):
    
    ax.scatter(
        df.index, df, 
        s = 30,
        alpha = 0.4, 
        color = 'gray'
        )
    
    ax.plot(
        df.index, 
        b.smooth2(df, 20), 
        lw = 2
        )
    
    ax.set(
        ylim = [0, 90], 
        yticks = np.arange(0, 100, 20),
        ylabel = b.y_label('vp')
        )
    return None 
    
def plot_wind(ax, df):
    
    ax.scatter(
        df.index, df, 
        s = 30,
        alpha = 0.4, 
        color = 'gray'
        )
    
    ax.plot(
        df.index, 
        b.smooth2(df, 20), 
        lw = 2
        )
    
    vmin, vmax, step = -20, 20, 5
    ax.set(
        ylim = [vmin, vmax], 
        yticks = np.arange(vmin, vmax + step, step),
        ylabel = b.y_label('UL')
        )
    
    
    ax.axhline(df.max(), linestyle = '--')
    ax.axhline(df.min(), linestyle = '--')


def plot_annual_GRT(df):

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
    
    ax[0].set(title = 2023)
    
    # b.format_month_axes(ax[-1])
    
    b.plot_letters(ax, y = 0.8, x = 0.02, 
                   fontsize = 20)
    return fig


def main():
    PATH_GAMMA = 'database/gamma/p1_saa.txt'
    
    df = b.load(PATH_GAMMA)

    
    
    # df = c.load_results('saa')
    df = df.loc[(df.index.time == dt.time(22, 0)) ]#&
    #             (df.index.year == 2015)]
    
    df['gr'] = df['ge'] / df['nui']
    print(df.describe()[['mer_perp', 'vp', 
                         'K', 'gr', 'gamma']])
    fig = plot_annual_GRT(df)
    
    FigureName = 'annual_grt_parameters'
    
    # fig.savefig(b.LATEX(
    #     FigureName, 
    #     folder = 'timeseries'), dpi = 400)



# main()

# plt.show()
