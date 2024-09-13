import matplotlib.pyplot as plt
import base as b
import datetime as dt
import numpy as np

b.config_labels(fontsize = 30)

PATH = 'database/indices/omni_hourly.txt'

def plot_kp(ax, ds, days = 2):
    
    if isinstance(ds, dt.datetime) :
        ds = indexes_in_range(ds, days = days)
        
    ax1 = ax.twinx()
    
    line, = ax1.plot(ds['f107'], lw = 2, color = 'red')
    
    b.change_axes_color(
            ax1, 
            color = line.get_color(),
            axis = "y", 
            position = "right"
            )
    
    vmax = ds['f107'].max()
    vmin = ds['f107'].min()
    ax1.set(
        ylim = [vmin - 5, vmax + 5],
        ylabel = '$F10,7$ (sfu)'
        )
    
    ds = ds.resample('3H').mean()
    ax.bar(
        ds.index, 
        ds['kp'], 
        width = 0.09,
        color = 'gray',
        alpha = 0.5, 
        edgecolor = 'k'
        )
    ax.set(
        ylabel = 'Kp', 
        ylim = [0, 12], 
        yticks = np.arange(0, 12, 3)
        )
    
    ax.axhline(3, lw = 2, color = 'k', linestyle = '--')
    
    return None 
    

def plot_dst(ax, ds, ylim = [-200, 100]):
    # print(ds.resample('1D').min()['dst'])
    ax.plot(ds['dst'], lw = 2)
    
    ax.set(
        xlim = [ds.index[0], ds.index[-1]], 
        ylim = [ylim[0] - 30, ylim[-1]],
        yticks = np.arange(ylim[0], ylim[-1] - 30, 50),
        ylabel = "Dst (nT)"
        )
    
    ax.axhline(0, lw = 0.5, color = 'k', linestyle = '-')
    
    for limit in [-50, -150]:
        ax.axhline(
            limit, 
            lw = 2, 
            color = 'k', 
            linestyle = '--'
            )
    return None 
        

def plot_magnetic_fields(ax, ds, ylim = 30):
    
    ax.plot(ds[['by', 'bz']], label = ['$B_y$', '$B_z$'] )
    
    ax.axhline(0, lw = 1, linestyle = '--', color = 'k')
    
    ax.set(
        ylim = [-ylim, ylim], 
        ylabel = '$B_y/B_z$ (nT)'
        )
    
    ax.legend(
        loc = 'upper right', 
        ncol = 2, 
        columnspacing = 0.5
        )
    
    return None 


    
def plot_auroras(ax, ds):
    
    ax.plot(ds[['al', 'ae']], label = ['AL', 'AE'])
    
    ax.set(
        yticks = np.arange(-2000, 3000, 1000),
        ylim = [-2000, 2000], 
        ylabel = 'AL/AE (nT)'
        )
    
    ax.axhline(0, lw = 1, linestyle = '--', color = 'k')
    
    ax.legend(
        loc = 'upper right', 
        ncol = 2, 
        columnspacing = 0.5
        )
    
    return None 


def indexes_in_range(dn, days = 2):
    
    ds = b.load(PATH)
    return b.range_dates(ds, dn, days = days)
    
def plot_one_day_indices(dn, days = 2):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (14, 14), 
        nrows = 4, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    ds = indexes_in_range(dn, days = 4)
   
    
    plot_magnetic_fields(ax[0], ds)
    plot_auroras(ax[1], ds)
    plot_kp(ax[2], ds)
    plot_dst(ax[3], ds)
    
    delta = dt.timedelta(hours = 3)
    ax[-1].set( 
       xlim = [ds.index[0] + delta, ds.index[-1] + delta], 
       xlabel = 'Dias'
       )
    
    month = b.monthToNum(dn.month, language = 'pt')
    year = dn.year
    ax[0].set(title = f'{month} de {year}')
    
    b.format_days_axes(ax[-1])
    
    delta = dt.timedelta(hours = 12)
    
    for a in ax.flat:
        a.axvspan(
            dn, dn + delta, 
            ymin = 0, ymax = 1,
            alpha = 0.2, 
            color = 'gray'
            )
    
    b.plot_letters(
        ax, 
        y = 0.8, 
        x = 0.03, 
        num2white = None
        )
    
    return fig 



dn = dt.datetime(2014, 2, 9, 21)
dn = dt.datetime(2019, 3, 19, 21)
dn = dt.datetime(2019, 5, 2, 21)
dn = dt.datetime(2016, 10, 3, 21)
dn = dt.datetime(2017, 8, 30, 21)
dn = dt.datetime(2014, 1, 2, 21)
dn = dt.datetime(2013, 3, 17, 21)
dn = dt.datetime(2022, 7, 24, 21)
dn = dt.datetime(2015, 12, 20, 21)

# dn = dt.datetime(2015, 12, 25, 21)
dn = dt.datetime(2019, 5, 2, 21)
# dn = dt.datetime(2019, 12, 6, 21)

def main():
    days = 3

    fig = plot_one_day_indices(dn, days = days)
    
    FigureName = dn.strftime('Indices_%Y%m%d')
    
    
    # fig.savefig(
    #       b.LATEX(FigureName, folder = 'timeseries'),
    #       dpi = 300
    #       )
    
# main()


