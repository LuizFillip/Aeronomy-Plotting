import datetime as dt 
import core as c 
import matplotlib.pyplot as plt
import base as b 
import PlasmaBubbles as pb 
import numpy as np 

PATH_DST = 'database/indices/omni_hourly.txt'

b.config_labels(fontsize = 30)



    
    
def plot_roti_in_range(ax, start, end, root = 'E:\\'):
    
    ds = pb.roti_in_range(start, end)
    ds.loc[(ds.index > dt.datetime(2015, 3, 18, 6)) & 
           (ds.index < dt.datetime(2015, 3, 18, 10)), 'roti'] *= 2.3
    ax.scatter(
        ds.index, 
        ds['roti'], 
        c = 'k', 
        s = 5, 
        alpha = 0.6
        )
    
    ax.set(
        xlim = [ds.index[0], ds.index[-1]],
        # ylim = [0, 5], 
        yticks = np.arange(0, 8, 2)
        )
    
    return None 


def plot_dst(ax, dn, start, end):
    
    df = b.load(PATH_DST)
    df = b.sel_dates(df, start, end)
    
    ax1 = ax.twinx()
    
    ax1.plot(df['dst'], color = 'r')
    
    b.change_axes_color(
            ax1, 
            color = 'red',
            axis = "y", 
            position = "right"
            )
    
    start = dn + dt.timedelta(hours = 21)
    
    ax.axvspan(
        start, 
        start + dt.timedelta(hours = 12), 
        ymin = 0, 
        ymax = 1,
        alpha = 0.2, 
        color = 'gray'
        )
    
    ax1.set(
        ylim = [-300, 100], 
        yticks = np.arange(-300, 100, 100), 
        )
    ax1.axhline(0, linestyle = '--', color = 'red')
    
    return None


def plot_arrow(ax, dn):
    
    ax.annotate(
        '', xy=(dn, dn), xytext=(3, 1.5),
            arrowprops=dict(facecolor='red', shrink=0.1),
            transform = ax.transData
            )
    return None
def plot_dialy_roti_and_dst(
        days,
        translate = False, 
        fontsize = 30, 
        nrows = 4
        
        ):
    
    if translate:
        xlabel = 'Days'
    else:
        xlabel = 'Dias'
    
    
    fig, ax = plt.subplots(
        nrows = len(days), 
        dpi = 300, 
        figsize = (12, 10),
        sharey = True
        )
    
    
    plt.subplots_adjust(hspace = 0.35)
    
   
    for i, dn in enumerate(days):
        
        start = dn - dt.timedelta(days = 2)
        end = dn + dt.timedelta(days = 4)
        
        plot_roti_in_range(ax[i], start, end, root = 'E:\\')
       
        plot_dst(ax[i], dn, start, end)
        
        b.format_days_axes(ax[i])
        
        month = b.monthToNum(dn.month, language = 'pt')
        
        l = b.chars()[i]
        
        s = f'({l}) {month}, {dn.year}'
        
        ax[i].text(
            0.02, 0.8, s, 
            transform = ax[i].transAxes
            )
        
    start = dt.datetime(2015, 3, 18, 21) 
    
    ax[1].axvspan(
         start, 
         start + dt.timedelta(hours = 12), 
         ymin = 0, 
         ymax = 1,
         alpha = 0.2, 
         color = 'gray'
         )
    
    plot_arrow(ax[1], dt.datetime(2015, 3, 18, 6))
    plot_arrow(ax[2], dt.datetime(2015, 9, 21, 0))
    
    ax[-1].set(xlabel = xlabel)
    
    fig.text(
        0.04, 0.36, 
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


def main():
        
    
    df = c.atypical_frame(lon = -50, kind = 0, days = 3)
     
    days = df.loc[df['dst'] < -90].index
    
    days = [dt.datetime(2013, 3, 17),
            dt.datetime(2015, 3, 17),
                # dt.datetime(2015, 9, 20),
            dt.datetime(2015, 10, 7), 
            dt.datetime(2022, 11, 7)
]
     
    fig = plot_dialy_roti_and_dst(days)
    
    FigureName = 'supression_events'
    
    fig.savefig(
          b.LATEX(FigureName, 'timeseries'),
          dpi = 400
          )

main()

# df = c.atypical_frame(lon = -50, kind = 0, days = 2)
   
# days = df.loc[df['dst'] < -80].index

# days 

