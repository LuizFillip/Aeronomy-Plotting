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
            cols = cols
            )
        
       
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
            '00:00', '20:00', include_end = False
            )
        
        df.iloc[idx] = df.iloc[idx].apply(lambda s: b.smooth2(s, 5))
        
        df = df.loc[~((df[site] > 50) | (df[site] < -20))]
        
        # print(df)
        
        def smooth_sections(df):
            
            time1 = (df.index.day == 21) | (df.index.day == 19)
           
            time2 = (
                (df.index > dt.datetime(2015, 12, 20, 6)) & 
                (df.index < dt.datetime(2015, 12, 21, 0))
                )
            
            time3 = (
                (df.index > dt.datetime(2015, 12, 21, 6)) & 
                (df.index < dt.datetime(2015, 12, 22, 0))
                )
            
            for time in [time1, time2]:
                df.loc[time]  = df.loc[time].interpolate(
                    order = 2, 
                    method = 'spline'
                    ) 
            
        smooth_sections(df)
        
        
        ax[i].plot(df, label = db_label, lw = 2)
    
        ax[i].set(
            ylim = [-40, 70], 
            yticks = np.arange(-40, 80, 20),
            xlim = [df.index[0], df.index[-1]]
            )
        
        s = b.chars()[i]
        
        name = dg.code_name(site)
        
        ax[i].text(
            0.02, 0.85, 
            f'({s}) {name}', 
            transform = ax[i].transAxes
            )
        

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
        bbox_to_anchor = (0.5, 1.6),
        loc = 'upper center', 
        ncols = 2
        )
    
    b.b.axes_hour_format(
         ax[-1], 
         hour_locator = 6, 
         tz = "UTC"
         )
    
    ax[-1].set(xlabel = 'Universal time')
    
    b.adding_dates_on_the_top(
            ax[0], 
            start = '2015-12-19', 
            end = '2015-12-23'
            )
    return fig


def main():
    sites = ['SAA0K',  'FZA0M',  'BVJ03', 'CAJ2M', 'CGK21'] #
    fig = plot_compare_quiet_disturbed_for_drift(sites, translate = True)
    
    FigureName = 'vertical_drift_comparation_time'
    
    path_to_save = 'G:\\Meu Drive\\Papers\\Case study - 21 december 2015\\June-2024-latex-templates\\'
    
    
    fig.savefig(path_to_save + FigureName, dpi = 400)
    
main()

