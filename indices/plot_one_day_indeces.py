import matplotlib.pyplot as plt
import base as b
import datetime as dt
import numpy as np
import PlasmaBubbles as pb 


b.sci_format(fontsize = 25)
PATH = 'database/indices/omni_hourly.txt'


def plot_dst(ax, ds, ylim = [-200, 100]):
    # print(ds.resample('1D').min()['dst'])
    ax.plot(ds['sym/h'], lw = 2)
    
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
    
    ax.plot(ds['by'], label = '$B_y$' )
    
    ax.axhline(0, lw = 1, linestyle = '--', color = 'k')
    
    ax1 = ax.twinx()
    
    ax1.plot(ds['bz'], color = '#0C5DA5',  label = '$B_z$')
    ax.set(
        ylim = [-ylim, ylim], 
        yticks = np.arange(-30, 40, 15),
        ylabel = '$B_y$ (nT)'
        )
    
    ax1.set(
        ylabel = '$B_z$ (nT)',
        yticks = np.arange(-30, 40, 15),
        ylim = [-ylim, ylim]
        )
    
    b.change_axes_color(
            ax1, 
            color = '#0C5DA5',
            axis = "y", 
            position = "right"
            )
    
    # ax.legend(
    #     loc = 'upper right', 
    #     ncol = 2, 
    #     columnspacing = 0.5
    #     )
    
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

def plot_epbs(ax, dn, sector = -50):
    
    df = pb.concat_files(
        dn, 
        days = 2, 
        root = 'E:\\', 
        hours = 12, 
        remove_noise = True
        )
    df = pb.filter_region(df, dn.year, sector)
    
    ax.plot(df['roti'])
    
    ax.set(ylim = [0, 2], ylabel = 'ROTI')


def plot_one_day_indices(dn, days = 2):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (14, 14), 
        nrows = 4, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    infile = 'database/indices/omni_high/20151'
    df = b.load(infile)

    ds = b.sel_times(df, dn, hours = 12) 
    
    ds =  ds.replace(9999.99, np.nan)
       
    plot_magnetic_fields(ax[0], ds)
    plot_auroras(ax[1], ds)
    plot_dst(ax[2], ds)
    plot_epbs(ax[-1], dn)
    
    month = b.monthToNum(dn.month, language = 'pt')
    year = dn.year
    ax[0].set(title = f'{month} de {year}')
    
    b.format_time_axes(
        ax[-1], hour_locator = 1, 
        translate = False)
    
    delta = dt.timedelta(hours = 12)
    
    for a in ax.flat:
        import plotting as pl 
        pl.plot_references_lines(
                a,
                -50, 
                dn, 
                label_top = None,
                translate = True
                )
        
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
dn = dt.datetime(2015, 12, 20, 20)

# dn = dt.datetime(2015, 12, 25, 21)
# dn = dt.datetime(2019, 5, 2, 21)
# dn = dt.datetime(2019, 12, 6, 21)

def main():
    days = 1

    fig = plot_one_day_indices(dn, days = days)
    
    FigureName = dn.strftime('Indices_%Y%m%d')
    
    
    # fig.savefig(
    #       b.LATEX(FigureName, folder = 'timeseries'),
    #       dpi = 300
    #       )
    
main()




