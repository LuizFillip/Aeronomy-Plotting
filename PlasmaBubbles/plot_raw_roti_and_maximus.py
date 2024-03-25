import matplotlib.pyplot as plt 
import base as b
import datetime as dt  
import PlasmaBubbles as pb 
import GEO as gg 
import numpy as np
import os 

b.config_labels()


args = dict(
     marker = 'o', 
     markersize = 3,
     linestyle = 'none', 
     color = 'gray', 
     alpha = 0.2, 
     )
    


def plot_roti_points(
        ax, ds, 
        threshold = 0.25,
        label = False, 
        points_max = True
        ):
        
    ax.plot(ds['roti'], **args, label = 'Pontos de ROTI')
    
    vmax = 3

    if len(ds) != 0:
        times = pb.time_range(ds)
        
        ax.axhline(
            threshold, 
            color = 'red', lw = 2, 
            label = f'{threshold} TECU/min'
            )
        
        df1 = pb.maximum_in_time_window(ds, 'max', times)
        
        if points_max:
            extra_args = dict(
                marker = 'o', 
                linestyle = 'none', 
                markersize = 3
                )
        else:
            extra_args = dict(markersize = 3)
        
        ax.plot(
            df1, 
            color = 'k',                
            label = 'Valor máximo',
            **extra_args
            )
        
        ax.set(yticks = np.arange(0, vmax + 2, 1))
        
        
        if label:
            ax.set(ylabel = 'ROTI (TECU/min)')
    
        return df1['max']

def plot_occurrence_events(ax, ds, threshold = 0.4):
    
    events = pb.events_by_longitude(ds, threshold)
    
    ax.plot(
          events, 
          marker = 'o',
          markersize = 3,
          color = 'k'
        )
    
    ax.set(
        yticks = [0, 1], 
        xlim = [ds.index[0], ds.index[-1]],
        ylim = [-0.2, 1.4]
        )
    
    for limit in [0, 1]:
        ax.axhline(
            limit, 
            color = 'k', 
            linestyle = '--'
            )
        
    return events
        


def plot_infos(ax, infos):
    
    delta = dt.timedelta(minutes = 10)
    
    for col, y in enumerate([3, 1.03]): 
        l = b.chars()[col]
        
        ax[0, col].text(
            -0.1, 1.3, f'({l})', 
            transform = ax[0, col].transAxes, 
            fontsize = 35
            )
        
        ax[0, col].text(
            infos[0] + delta, y, 'Anoitecer', 
            transform = ax[0, col].transData
            )
        
        ax[0, col].text(
            infos[1] + delta, y, 'Meia noite local', 
            transform = ax[0, col].transData
            )

def plot_row_roti_in_sectors(
        df, dn, 
        threshold = 0.25,
        fontsize = 30):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 4,
        ncols = 2, 
        sharex = True,
        figsize = (18, 12)
        )
    
    plt.subplots_adjust(hspace = 0.3, wspace = 0.03)
    
    coords = gg.set_coords(dn.year)
    
    out_infos = []
    for row, sector in enumerate(coords.keys()):
    
        ds = pb.filter_coords(df, sector, coords)
        
        ds = plot_roti_points(
                ax[row, 0], ds, 
                threshold = threshold,
                label = False, 
                points_max = True
                )
        
        terminator = pb.terminator(sector, dn, float_fmt = False)
        
        ax[row, 1].axvline(terminator, color = 'k', lw = 2)
        ax[row, 0].axvline(terminator, color = 'k', lw = 2)
        
        plot_occurrence_events(ax[row, 1], ds, threshold)
        
        ax[row, 1].yaxis.tick_right()
        
        info = f'Setor {row + 1} ({sector}°)'
        
        ax[row, 0].text(
            0.9, 1.1, info, 
            transform = ax[row, 0].transAxes
            )
        
        delta = dt.timedelta(hours = 3)
        midnight = gg.local_midnight(dn + delta, sector)
        
        ax[row, 1].axvline(midnight, color = 'b', lw = 2)
        ax[row, 0].axvline(midnight, color = 'b', lw = 2)
        
        if row == 0:
            out_infos.extend([terminator, midnight])
  
    plot_infos(ax, out_infos)
    
    b.format_time_axes(ax[-1, 0], translate = True)
    b.format_time_axes(ax[-1, 1], translate = True)
    
    
    fig.text(0.07, 0.33, 'ROTI (TECU/min)', 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(0.93, 0.42, 'Ocorrência', 
        fontsize = fontsize, 
        rotation = 'vertical'
        ) 
    
    return fig 



def main():
    dn = dt.datetime(2014, 2, 9, 21)
    
    
    df = pb.concat_files(
        dn, 
        days = 2, 
        root = os.getcwd(), 
        hours = 12
        )
    
    df = df.loc[~df['sts'].isin(['mabb'])] 
    
    fig = plot_row_roti_in_sectors(
            df, dn, threshold = 0.25,
            fontsize = 30)
    
    
    FigureName = dn.strftime('%Y%m%d_midnight_event')
     
    fig.savefig(
          b.LATEX(FigureName, 
          folder = 'timeseries'),
          dpi = 400
          )
    
# main()