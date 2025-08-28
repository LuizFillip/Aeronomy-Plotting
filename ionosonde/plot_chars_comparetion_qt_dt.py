import matplotlib.pyplot as plt
import datetime as dt 
import digisonde as dg 
import base as b 
from matplotlib.ticker import MultipleLocator

b.sci_format()



def plot_compare_quiet_disturbed_for_chars(
        sites, parameter = 'hF', cols = [5, 6]
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
    
     #'hmF2'
    
    for i, site in enumerate(sites):
     
        name = dg.code_name(site)
        
        s = b.chars()[i]
        
        ax[i].text(
            0.02, 0.8, 
            f'({s}) {name}', 
            transform = ax[i].transAxes
            )
     
    
        qt = dg.repeat_quiet_days(
             site, 
             start, 
             parameter, 
             cols = cols, 
             window = 10
             )
        
        for col in qt.columns:
            qt[col] = b.smooth2(qt[col], 10)
    
        ax[i].plot(
            qt.index, 
            qt['mean'], 
            color = 'purple', 
            lw = 2
            )
        
        ax[i].fill_between(
            qt.index, 
            qt['mean'] - qt['std'], 
            qt['mean'] + qt['std'], 
            color = "purple", 
            alpha = 0.3
            )
    
        df = dg.join_iono_days(
                site, 
                start,
                parameter,
                cols = cols, 
                window = window
                )
        
        df.iloc[:, 0] = b.smooth2(df.iloc[:, 0], 3)
        ax[i].plot(df, lw = 2)
        
        ax[i].set(xlim = [df.index[0], df.index[-1]])
        
        
    b.format_time_axes(
         ax[-1], 
         hour_locator = 12, 
         translate = True, 
         pad = 85, 
         format_date = '%d/%m/%y'
         )
    
    
    # major ticks de 1h
    major_tick = 0.5
    subdivison =  4
    ax[-1].xaxis.set_major_locator(MultipleLocator(major_tick))
    # minor ticks: 4 subdivisões por intervalo → 1/4 = 0.25
    ax[-1].xaxis.set_minor_locator(MultipleLocator(major_tick / subdivison))
    
    return fig 


sites = [ 'SAA0K', 'BVJ03', 'CAJ2M', 'CGK21']

fig = plot_compare_quiet_disturbed_for_chars(sites)