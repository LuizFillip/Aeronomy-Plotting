import matplotlib.pyplot as plt
import datetime as dt 
import numpy as np 
import digisonde as dg 
import base as b 
import plotting as pl


b.sci_format()

def plot_compare_quiet_disturbed(
        sites, 
        translate = False
        ):
    
    if translate:
        ylabel = 'Vertical drift (m/s)'
        qt_label = 'Quiet-time'
        db_label = 'Storm-time'
    else:
        ylabel = 'Velocidade de deriva vertical (m/s)'
        qt_label = 'Período calmo'
        db_label = 'Período perturbado'
    
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = len(sites),
        figsize = (16, 18), 
        sharex = True, 
        sharey = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    start = dt.datetime(2015, 12, 19)
    # cols = list(range(3, 10, 1))
    cols = [5, 6]
 
    for i, site in enumerate(sites):
        
        
        
        ref_day = dt.datetime(2015, 12, 20, 21, 0)
        
        ax[i].axvspan(
             ref_day, 
             ref_day + dt.timedelta(hours = 12), 
             ymin = 0, 
             ymax = 1,
             alpha = 0.2, 
             color = 'gray'
             )
        
        if site == 'BVJ03':
            window = 3
        else:
            window = 2
            
        qt = dg.repeat_quiet_days(
            site, 
            start, 
            parameter = 'drift', 
            cols = cols, 
            window = window + 1
            )
        
        qt = qt[~qt.index.duplicated(keep="first")]

        qt = qt.resample('30min').asfreq()
        
        ax[i].errorbar(
            qt.index,
            qt['vz'],
            yerr = qt['svz'], 
            label = qt_label, 
            capsize = 5
            )
        
        # ax[i].fill_between(
        #     qt.index, 
        #     qt['vz'] - qt['svz'], 
        #     qt['vz'] + qt['svz'], 
        #     color = "gray", 
        #     alpha = 0.4
        #     )

    
        df = dg.join_iono_days(
                site, 
                start,
                cols = cols, 
                window = window
                )
        
        df = df[~df.index.duplicated(keep = "first")]
        
        df = df.resample('30min').asfreq()
        
        
        # if site in ['BVJ03', 'CAJ2M', 'CGK21']:
            
        #     df[site] = b.smooth2(df[site], 2)
        
        ax[i].plot(df, label = db_label, lw = 2)
    
        ax[i].set(
            ylim = [-60, 60], 
            yticks = np.arange(-50, 60, 20),
            xlim = [df.index[0], df.index[-1]]
            )
        
        s = b.chars()[i]
        
        name = dg.code_name(site)
        
        ax[i].text(
            0.02, 0.85, 
            f'({s}) {name}', 
            transform = ax[i].transAxes
            )
        
        pl.plot_terminators(ax[i], df, site)
        
        ax[i].axhline(0, linestyle = ':')
        ax[i].axhline(40, linestyle = ':')
        
    fig.text(
        0.03, 0.4, 
        ylabel, 
        fontsize = 35, 
        rotation = 'vertical'
        )
    

    ax[0].legend(
        bbox_to_anchor = (0.5, 1.4),
        loc = 'upper center', 
        ncols = 2
        )
    
    b.format_time_axes(
        ax[-1], 
        hour_locator = 12, 
        translate = translate, 
        pad = 85, 
        format_date = '%d/%m/%y'
        )
    
    return fig


def main():
    sites = ['SAA0K',  'FZA0M',  'CAJ2M', 'CGK21'] #
    fig = plot_compare_quiet_disturbed(sites, translate = True)
    
    FigureName = 'quiet_disturbance_time'
    
    # path_to_save = 'G:\\My Drive\\Papers\\Paper 2\\Geomagnetic control on EPBs\\June-2024-latex-templates\\'
    
    
    # fig.savefig(path_to_save + FigureName, dpi = 400)
    
main()

