import PlasmaBubbles as pb 
import base as b 
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 
import datetime as dt
import GEO as gg 

b.config_labels(fontsize = 22)

PATH_INDEX =  'database/indices/omni_pro.txt'

def plot_terminator(ax, df, lon):
    
    ax.plot(df.index, df['dusk'], lw = 2, color = 'w')
    
    dn = df.index[0]
    
    midnight = gg.local_midnight(dn, lon, delta_day = None)
    midnight = round(b.dn2float(midnight))
    ax.axhline(midnight, lw = 2, color = 'w')

    ax.text(
        0.01, 0.05, 
        'Solar terminator (300 km)', 
        color = 'w',
        transform = ax.transAxes
        )
    
    ax.text(
         dn, midnight + 0.5, 
        'Local midnight', 
        color = 'w',
        transform = ax.transData
        )
    
    ax.plot(df.index, df['dusk'] + 2,
            linestyle = '--', 
            lw = 2, color = 'w')
    
def plot_seasonal_hourly(
        ax,
        df2, 
        cmap = 'jet',
        fontsize = 35, 
        translate = False,
        factor = 100,
        percent = True,
        heatmap = True, 
        colorbar = True
        ):
    
    if translate:
        xlabel = 'Years'
        ylabel = 'Universal time'
        zlabel = 'Occurrence (\%)'
    else:
        xlabel = 'Anos'
        ylabel = 'Hora universal'
        zlabel = 'Ocorrência (\%)'
   
    yticks = df2.index 
    xticks = df2.columns 
    values = df2.values
    
    if heatmap:
        img = ax.imshow(
              values[::-1],
              aspect = 'auto', 
              extent = [xticks[0], xticks[-1], 
                        yticks[0], yticks[-1]],
              cmap = cmap
              )
    else:
    
        img = ax.contourf(
            xticks, 
            yticks, 
            values, 
            60, 
            cmap = cmap        
            )

    ticks =  np.arange(0, 1.25 * factor, 0.25 * factor)
    
    if colorbar:
        b.colorbar(
            img, 
            ax,
            ticks = ticks, 
            label = zlabel, 
            anchor = (.08, 0., 1, 1)
            )
        
   
    
    print(yticks)
    
    yticks = np.arange(yticks[0], yticks[-1] + 2, 2)
 
    xticks = pd.date_range(xticks[0], xticks[-1], periods = 10)
    xticklabels = [t.year for t in xticks]
    ax.set(
           yticks = yticks,
           xticks = xticks,
           xlim = [xticks[0], xticks[-1]],
           # xlim = [xticks[0], xticks[-1]],
            xticklabels = xticklabels,
           # xlabel = xlabel,
           ylabel = ylabel
       )
    return ax


def plot_f107(ax, limit = 84.33):
    
    df = b.load(PATH_INDEX)

    df["f107a"] = df["f107"].rolling(
        window = 81).mean(center = True)
    
    df = b.sel_dates(
        df, 
        dt.datetime(2013, 1, 1), 
        dt.datetime(2022, 12, 21)
        )


    ax.plot( df["f107"])
    ax.plot( 
        df["f107a"], 
        lw = 3, color = 'cornflowerblue', 
        label = '81 days average'
        )
        
    ax.set(
        ylabel = '$F_{10.7}$ (sfu)', 
        ylim = [50, 250],
        yticks = np.arange(60, 350, 50),
        xlabel = 'Years'
        )


    ax.axhline(
        limit, 
        lw = 2, 
        color = 'r', 
        label = f'{limit} sfu'
        )
    
    ax.legend(loc = 'upper right')
        



def plot_annual_hourly(df, sector = -50):

    df2 = pb.hourly_annual_distribution(df, step = 1)
    
    
    fig, ax = plt.subplots(
              dpi = 300, 
              nrows = 2,
               sharex = True, 
              figsize = (12, 8)
              )
    
    
    plt.subplots_adjust(hspace = 0.1)
    plot_f107(ax[1])
    
    
    plot_seasonal_hourly(
        ax[0],
        df2, 
        cmap = 'jet',
        fontsize = 35, 
        translate = True,
        heatmap = False
        )
    
    plot_terminator(ax[0], df, sector)
    
    
    b.plot_letters(
        ax, y = 0.85, x = 0.03,
        num2white = [0]
        )
    
    return fig


def main():

    ds = b.load('events_class2')
    
    df = ds.loc[(ds['lon'] == -50) & (ds.index.year < 2023)] 
    
    fig = plot_annual_hourly(df)
    
    FigureName = 'hourly_annual_variation'
      
    # fig.savefig(
    #         b.LATEX(FigureName, folder = 'paper2'),
    #         dpi = 400
    #         ) 
    
    
main()