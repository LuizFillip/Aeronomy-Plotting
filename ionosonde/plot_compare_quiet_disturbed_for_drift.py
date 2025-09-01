import matplotlib.pyplot as plt
import datetime as dt 
import numpy as np 
import digisonde as dg 
import base as b 
import plotting as pl


b.sci_format(fontsize = 30)

def plot_compare_quiet_disturbed_for_drift(
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
    cols = [5, 6, 7]
 
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
        
        # for col in qt.columns:
        #     qt[col] = b.smooth2(qt[col], 10)
        
        qt = qt.apply(lambda s: b.smooth2(s, 10))
        
        ax[i].plot(
            qt.index,
            qt['vz'], 
            color = 'purple', 
            lw = 2, 
            label = 'Quiet-time'
            )
        
        ax[i].fill_between(
            qt.index, 
            qt['vz'] - qt['svz'], 
            qt['vz'] + qt['svz'], 
            color = "purple", 
            alpha = 0.3
            )

    
        df = dg.join_iono_days(
                site, 
                start,
                cols = cols, 
                window = window
                )
        
        idx = df.index.indexer_between_time(
            '00:00', '20:00', include_end=False)

        df.iloc[idx] = df.iloc[idx].apply(lambda s: b.smooth2(s, 5))
        
        ax[i].plot(df.interpolate(), label = db_label, lw = 2)
    
        ax[i].set(
            ylim = [-70, 70], 
            yticks = np.arange(-60, 80, 20),
            xlim = [df.index[0], df.index[-1]]
            )
        
        s = b.chars()[i]
        
        name = dg.code_name(site)
        
        ax[i].text(
            0.02, 0.85, 
            f'({s}) {name}', 
            transform = ax[i].transAxes
            )
        
        # pl.plot_terminators(ax[i], df, site)
        
        dates = (np.unique(df.index.date))
            
        for dn in dates:
            ax[i].axvline(dn, lw = 1, linestyle = '--')
        
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
    sites = ['SAA0K',  'FZA0M',  'BVJ03', 'CAJ2M', 'CGK21'] #
    fig = plot_compare_quiet_disturbed_for_drift(sites, translate = True)
    
    FigureName = 'quiet_disturbance_time'
    
    # path_to_save = 'G:\\My Drive\\Papers\\Paper 2\\Geomagnetic control on EPBs\\June-2024-latex-templates\\'
    
    
    # fig.savefig(path_to_save + FigureName, dpi = 400)
    
main()

