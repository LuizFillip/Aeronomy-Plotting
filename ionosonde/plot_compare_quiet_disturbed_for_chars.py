import matplotlib.pyplot as plt
import datetime as dt 
import digisonde as dg 
import base as b 
import numpy as np 

b.sci_format(fontsize = 30)

def plot_quiettime(ax, site, parameter, start):

    qt = dg.repeat_quiet_days(
         site, 
         start, 
         parameter, 
         )
    
    qt = qt.apply(lambda s: b.smooth2(s, 3))

    ax.plot(
        qt.index, 
        qt['mean'], 
        color = 'purple', 
        lw = 2, 
        label = 'Quiet-time'
        )
    
    ax.fill_between(
        qt.index, 
        qt['mean'] - qt['std'], 
        qt['mean'] + qt['std'], 
        color = "purple", 
        alpha = 0.3
        )
    
    return None 

def plot_compare_quiet_disturbed_for_chars(
        sites, 
        parameter = 'hF', cols = [5, 6]
        ):

    nrows = len(sites)
     
     
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = nrows,
        figsize = (14, nrows * 3), 
        sharex = True, 
        sharey = True
        )
    
    start = dt.datetime(2015, 12, 19)
   
    plt.subplots_adjust(hspace = 0.1)
    window = 3
    
    
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
     
        name = dg.code_name(site)
        
        s = b.chars()[i]
        
        ax[i].text(
            0.02, 0.8, 
            f'({s}) {name}', 
            transform = ax[i].transAxes
            )
        
        
        plot_quiettime(ax[i], site, parameter, start)
        
        df = dg.join_iono_days(
                site, 
                start,
                parameter,
                cols = cols, 
                window = window
                )
        
        
        ax1 = ax[i].twinx()
        ax1.bar(
            df.index, 
            df['QF'], 
            width = 0.03, 
            alpha = 0.5, 
            color = 'gray'
            ) 
        ax1.set(
            ylim = [0, 60], 
            yticks = np.arange(10, 80, 20)
            )
        
        df[parameter] = b.smooth2(df[parameter], 3)
        ax[i].plot(
            df[parameter].interpolate(), 
            lw = 2, label = 'Storm-time'
            )
        
        ax[i].set(xlim = [df.index[0], df.index[-1]])
    
        dates = (np.unique(df.index.date))
        
        ax[i].set(
            ylim = [0, 700], 
            yticks = np.arange(0, 800, 200)
            )
        for dn in dates:
            ax[i].axvline(dn, lw = 1, linestyle = '--')
    
    fontsize = 30
    
    ax[0].legend(
        loc = 'upper center', ncol = 2, 
        bbox_to_anchor = (0.5, 1.4)
              )
    
    fig.text(
        0.03, 0.4, 
        'Virtual height (km)', 
        fontsize = fontsize + 5, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.95, 0.38, 
        'Range Spread F (km)', 
        fontsize = fontsize + 5, 
        rotation = 'vertical'
        )
    
    b.format_time_axes(
         ax[-1], 
         hour_locator = 6, 
         translate = True, 
         pad = 85, 
         format_date = '%d/%m/%y'
         )
    
    return fig 


sites = [ 'SAA0K', 'FZA0M', 'BVJ03', 'CAJ2M', 'CGK21']

fig = plot_compare_quiet_disturbed_for_chars(sites,  parameter = 'hmF2')

path_to_save = 'G:\\Meu Drive\\Papers\\Case study - 21 december 2015\\June-2024-latex-templates\\'

FigureName = 'hmF2_comparation_time'
  

# fig.savefig(path_to_save + FigureName, dpi = 400)
  