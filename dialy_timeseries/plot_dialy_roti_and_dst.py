import datetime as dt 
import core as c 
import matplotlib.pyplot as plt
import base as b 

PATH_EPB = 'database/epbs/longs/'
PATH_DST = 'database/indices/omni_hourly.txt'

b.config_labels()

def plot_dialy_roti_and_dst():
    
    fig, ax = plt.subplots(
        nrows = 5, 
        dpi = 300, 
        figsize = (12, 10),
        sharey = True
        )
    
    
    plt.subplots_adjust(hspace = 0.8)
    
    df = c.atypical_frame(lon = -50, kind = 0, days = 3)
    days = df.loc[df['dst'] < -90]
    
    print(days)
    for row, dn in enumerate(days.index[:5]):
        
        start = dn - dt.timedelta(days = 2)
        end = dn + dt.timedelta(days = 4)
        
        ds = b.sel_dates(
            b.load(f'{PATH_EPB}{dn.year}'), 
            start, end)
        
        df = b.sel_dates(
            b.load(PATH_DST), 
            start, end
            )
        ax[row].plot(ds['-50'])
        ax1 = ax[row].twinx()
        
        ax1.plot(df['dst'], color = 'r')
        b.change_axes_color(
                ax1, 
                color = 'red',
                axis = "y", 
                position = "right"
                )
        
        start = dn + dt.timedelta(hours = 21)
        ax[row].axvspan(
            start, 
            start + dt.timedelta(hours = 12), 
            ymin = 0, 
            ymax = 1,
            alpha = 0.2, 
            color = 'gray'
            )
        
        b.format_days_axes(ax[row])
        
        ax1.set(ylim = [-250, 80], 
                title = dn.strftime('%B, %Y'))
        
        ax[row].set(ylim = [0, 3])
    ax[-1].set(xlabel = 'Days')
    
    fontsize = 30
    fig.text(
        0.03, 0.35, 
        'ROTI (TECU/min)', 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.99, 0.4, 
        'Dst (nT)', 
        fontsize = fontsize, 
        rotation = 'vertical',
        color = 'r'
        )
    return fig 

fig = plot_dialy_roti_and_dst()

FigureName = 'supression_events'
fig.savefig(
      b.LATEX(FigureName, 'timeseries'),
      dpi = 400
      )
