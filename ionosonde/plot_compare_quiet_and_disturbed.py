import matplotlib.pyplot as plt
import datetime as dt 
import numpy as np 
import digisonde as dg 
import base as b 
import plotting as pl


b.config_labels()

def plot_compare_quiet_disturbed(
        translate = False
        ):
    
    if translate:
        ylabel = 'Vertical drift (m/s)'
        qt_label = 'Quiet time'
        db_label = 'Disturbance time'
    else:
        ylabel = 'Velocidade de deriva vertical (m/s)'
        qt_label = 'Período calmo'
        db_label = 'Período perturbado'
        
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        figsize = (16, 10), 
        sharex = True, 
        sharey = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    start = dt.datetime(2015, 12, 19)
    cols = list(range(3, 10, 1))
    
    sites = ['SAA0K', 'BVJ03'] #'CAJ2M']

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
                smooth = 3
                )
        
        df = df.interpolate()
        
        df[site] = b.smooth2(df[site], 3)
        
        ax[i].plot(df, label = db_label, lw = 2)
    
        ax[i].set(
            ylim = [-20, 45], 
            yticks = np.arange(-20, 50, 20),
            xlim = [df.index[0], df.index[-1]]
            )
        
        s = b.chars()[i]
        name = dg.code_name(site)
        ax[i].text(
            0.02, 0.8, 
            f'({s}) {name}', 
            transform = ax[i].transAxes
            )
        
        pl.plot_terminators(ax[i], df, site)
        
        ax[i].axhline(0, linestyle = ':')
              
    fig.text(
        0.03, 0.2, 
        ylabel, 
        fontsize = 35, 
        rotation = 'vertical'
        )
    

    ax[0].legend(
        bbox_to_anchor = (0.5, 1.32),
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
    
    fig = plot_compare_quiet_disturbed(translate= True)
    
    FigureName = 'quiet_disturbance_time'
    
    path_to_save = 'G:\\My Drive\\Papers\\Paper 2\\Geomagnetic control on EPBs\\June-2024-latex-templates\\'
    
    
    fig.savefig(path_to_save + FigureName, dpi = 400)
    
# main()
