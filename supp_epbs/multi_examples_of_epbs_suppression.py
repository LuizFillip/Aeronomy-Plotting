import matplotlib.pyplot as plt 
import plotting as pl 
import datetime as dt 
import base as b 
import core as c
import GEO as gg 
import numpy as np 


def plot_sym_h(ax, dn, days = 3):
    
    ds = c.high_omni(dn.year)
    ds = b.range_dates(ds, dn, days = days)
    st = c.find_storm_interval(ds['sym'])
   
    ax1 = ax.twinx()

    pl.plot_dst(ax1, ds, color = 'red')
    
    b.change_axes_color(
            ax1, 
            color = 'red',
            axis = "y", 
            position = "right"
            )
    
    return np.unique(ds.index.date), st 

def set_axis(ax):
    b.axes_hour_format(
         ax, 
         hour_locator = 6, 
         tz = "UTC"
         )
    
    b.adding_dates_on_the_top(
            ax, 
            fmt = '%d/%m/%y', 
            pad = -30
            )
    
    return None




def plot_single_case(ax, dn, days = 4):
    dusk = gg.terminator(-50, dn, float_fmt = False)
    
    dates, st =  plot_sym_h(ax, dn, days = days)
    
    delta = dt.timedelta(days = 2)
    start = dates[0] + delta
    
    end = dates[-1] 
    
    dns = pl.plot_roti_in_range(ax, start, end)
       
    estart, emiddle, eend = tuple(st)
    
    pl.plot_reference_lines(ax, dusk, estart, eend, dns)
    
    pl.plot_arrow_and_note(ax, estart, eend, y = -100)
    
    set_axis(ax)
    
    ax.set(
        # ylabel = '',
        xlim = [start, end]
        )
    
    return None 
    
    
def plot_multi_examples_of_suppression(dates):
    nrows = len(dates)
    
    fig, ax = plt.subplots(
        dpi = 300, 
        sharey = True,
        figsize = (16, 3 * nrows), 
        nrows = nrows
        )
    
    for i, dn in enumerate(dates):
        
        plot_single_case(ax[i], dn)
        
        if i < nrows - 1:
            ax[i].set(xticklabels = [])
        
    
    fig.align_ylabels()
    
    ax[-1].set(xlabel = 'Universal time')
    
    b.plot_letters(
        ax, 
        y = 1.02, 
        x = 0., 
        fontsize = 25
        )

    return fig

def main():
    
    dates = [ 
        dt.datetime(2013, 3, 17),
        dt.datetime(2014, 9, 9),
        dt.datetime(2017, 3, 1),
        dt.datetime(2016, 3, 14),
        dt.datetime(2022, 10, 3)
        ]
    
    df = b.load('core/src/geomag/data/stormsphase')

    df = c.geomagnetic_analysis(df)

    dates = df.loc[df.category == 'quiet'].index[20:25]
    
    fig = plot_multi_examples_of_suppression(dates)
    
    path_to_save = 'G:\\Meu Drive\\Papers\\SuppressionAnalysis\\June-2024-latex-templates\\'
    
    FigureName = 'multi_examples_of_epbs_suppression'
    
    
    # fig.savefig(path_to_save + FigureName, dpi = 300)
    
main()