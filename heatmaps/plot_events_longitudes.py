import matplotlib.pyplot as plt
import seaborn as sns  
import base as b
import pandas as pd
import datetime as dt
import PlasmaBubbles as pb 

PATH_EVENT = 'D:\\database\\epbs\\events\\'


def heat_map_for_events(
        df, 
        freq = '1h'
        ):
        
    df.columns = pd.DatetimeIndex(
        df.columns).strftime('%H:00')
    
    fig, ax = plt.subplots(
        figsize = (12, 8), 
        dpi = 300
        )
    
    b.config_labels()
    xticks_spacing = (int(pd.Timedelta(freq) /
                          pd.Timedelta('30s')))
    
    sns.heatmap(
        df, 
        ax = ax,
        linecolor='white',
        vmax = 1,
        vmin = 0,
        cbar_kws = {
        'pad': .02, 
        'ticks': [0, 1],
        },
        xticklabels = xticks_spacing
        )
    
    ax.set(ylabel = 'Longitudes', 
            xlabel = 'Universal time')
        
    value_to_int = {j: i for i, j in
                    enumerate(['non EPB', 'EPB'])}

    n = len(value_to_int)     
    
    colorbar = ax.collections[0].colorbar 
    r = colorbar.vmax - colorbar.vmin 
    colorbar.set_ticks([colorbar.vmin + 
                        r * i for i in range(n)])
    colorbar.set_ticklabels(list(value_to_int.keys()))   

    return 


 
def get_date_range(ds):
    delta = dt.timedelta(hours = 20)
    s = pd.to_datetime(ds.index[0].date()) + delta 
    e = ds.index[-1].date() + delta 
    
    return pd.date_range(s, e, freq = '1D')


def main():
    
    dn = dt.datetime(2014, 1, 1, 20)
    
    ds = b.load(
        pb.epb_path(
            dn.year, 
            path = 'events'
            )
        )
    
    ds = b.sel_times(ds, dn)
    
    
    heat_map_for_events(
            ds.T, 
            freq = '1h'
            )
    
    



def plot_hourly_and_histograms(
        ds,
        translate = False, 
        fontsize = 45
        ):
    
    

    fig, ax = plt.subplots(
           ncols = 1,
           nrows = 4,
           dpi = 300, 
           sharex = True, 
           sharey = True,
           figsize = (18, 14)
           )
    
    
    plt.subplots_adjust(hspace = 0.1)
    values = pb.annual_hourly_all_sectors(
            ds, 
            normalize = True,
            step = 1, 
            percent = True
        )
    
    
    xticks, yticks = get_ticks(values, ds, step = 1)
  
    sectors = list(range(-80, -40, 10))[::-1]
    
    
    for i, sector in enumerate(sectors):
        
        ds1 = ds.loc[ds['lon'] == sector]
            
        ax[i].imshow(
              values[i],
              aspect = 'auto', 
              extent = [xticks[0], xticks[-1], 
                        yticks[0], yticks[-1]],
              cmap = 'jet', 
              vmax = 100, 
              vmin = 0
              )
        
        # plot_histogram(ax[i], ds1['start'].values, i)

        ax[i].set(xlim = [xticks[0], xticks[-1]])
        # pl.plot_terminator(ax[i], sector, translate = False)
        
        l = b.chars()[i]
        s = f'({l}) Setor {i + 1}'
        
        ax[i].text(
            0.01, 0.82, s, 
            transform = ax[i].transAxes, 
            color = 'w',
            fontsize = 35
            )
        
    if translate:
        ylabel = 'Universal time'
        xlabel = 'Years'
        zlabel = 'Occurrence (\%)'
    else:
        xlabel = 'Anos'
        ylabel = 'Hora universal'
        zlabel = 'Ocorrência (\%)'
        
    b.fig_colorbar(
            fig,
            vmin = 0, 
            vmax = 100, 
            cmap = 'jet',
            fontsize = 35,
            step = 10,
            label = zlabel, 
            sets = [0.32, 0.96, 0.4, 0.02], 
            orientation = 'horizontal', 
            levels = 10
            )

    
    ax[-1].set_xlabel(xlabel, fontsize = fontsize)
    
    fig.text(
        0.05, 0.38, 
        ylabel, 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    return fig 

