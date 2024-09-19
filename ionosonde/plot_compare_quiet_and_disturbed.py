import GEO as gg 
import matplotlib.pyplot as plt
import datetime as dt 
import numpy as np 
import digisonde as dg 
import base as b 
import pandas as pd


def plot_terminators(ax, df, site):
    
    #     for i in range(number):
            
    #         delta = dt.timedelta(days = 1)
            
    
    for dn in np.unique(df.index.date):
        
        dusk = gg.dusk_from_site(
                pd.to_datetime(dn), 
                site = site[:3].lower(),
                twilight_angle = 18
                )
        
        ax.axvline(
            dusk, 
            lw = 2, 
            linestyle = '--', 
            color = 'k'
            )
        
        
# def plot_dusk_time(ax, start, number = 4):
    


def plot_compare_quiet_disturbed(
        translate = False
        ):
    
    if translate:
        ylabel = 'Vertical drift (m/s)'
        qt_label = 'Quiet time'
        db_label = 'Disturbance time'
    else:
        ylabel = 'Deriva vertical (m/s)'
        qt_label = 'Período calmo'
        db_label = 'Período perturbado'
        
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 3,
        figsize = (16, 12), 
        sharex = True, 
        sharey = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    start = dt.datetime(2015, 12, 19)
    cols = np.arange(2, 7, 1)
    
    sites = ['SAA0K', 'BVJ03', 'CAJ2M']

    for i, site in enumerate(sites):
        
        ref = dt.datetime(2015, 12, 20, 21, 0)
        
        ax[i].axvspan(
             ref, 
             ref + dt.timedelta(hours = 12), 
             ymin = 0, 
             ymax = 1,
             alpha = 0.2, 
             color = 'gray'
             )
        
        qt = dg.repeat_quiet_days(site,  start)
        
        ax[i].plot(qt, label = qt_label)
    
        df = dg.join_iono_days(
                site, 
                start,
                cols = cols, 
                smooth = None 
                )
        
        df = df.interpolate()
        
        df[site] = b.smooth2(df[site], 10)
        
        ax[i].plot(df, label = db_label)
    
        ax[i].set(
            ylim = [-20, 43], 
            yticks = np.arange(-20, 50, 20),
            xlim = [df.index[0], df.index[-1]]
            )
        
        s = b.chars()[i]
        name = dg.code_name(site)
        ax[i].text(
            0.02, 0.75, 
            f'({s}) {name}', 
            transform = ax[i].transAxes
            )
        
        plot_terminators(ax[i], df, site)
        
        ax[i].axhline(0, linestyle = ':')
              
    ax[1].set_ylabel(ylabel, fontsize = 35)
    

    ax[0].legend(
        bbox_to_anchor = (0.5, 1.35),
        loc = 'upper center', 
        ncols = 2)
    
    b.format_time_axes(
        ax[-1], hour_locator = 12, 
        translate = translate, 
        pad = 80)
    return fig


def main():
    
    fig = plot_compare_quiet_disturbed()
    
    FigureName = 'quiet_disturbance_time'
    
    fig.savefig(b.LATEX(FigureName, 'Iono'), dpi = 400)
    
main()