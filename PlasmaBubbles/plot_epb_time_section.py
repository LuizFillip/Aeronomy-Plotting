import matplotlib.pyplot as plt
import base as b 
import pandas as pd 
import numpy as np
import datetime as dt 
import plotting as pl 


b.config_labels(fontsize = 30)



def shade_area(
        ax, 
        start,
        end,
        name = 'Daytime', 
        color = '#0C5DA5'
        ):
    
    ax.axvspan(
        start, end, 
        ymin = 0, 
        ymax = 1,
        alpha = 0.2, 
        color = color
        )
    
    
    return None


def dumb_data(start):
    
    end = start + dt.timedelta(hours = 11)
    time = pd.date_range(start, end, freq = '1min')
    return pd.DataFrame(
        {'Occ': np.zeros(len(time))}, index = time)




def plot_region_shades(
        ax, 
        sector, 
        dn, 
        label_top = 1.05,  
        translate = False
        ):
    
    if translate:
        midn_name = 'Post-midnight'
        term_name = 'Post-sunset' 
    else:
        term_name = 'Pós-pôr do sol'
        midn_name = 'Pós-meia-noite'
    
        
    dusk, midnight = pl.plot_references_lines(
            ax,
            sector, 
            dn, 
            label_top = label_top,
            translate = translate
            )
    
    end_sunset = dusk + dt.timedelta(hours = 2)
    shade_area(
            ax, 
            dusk,
            end_sunset,
            name = term_name,
            color = '#0C5DA5'
            )
    
    
    delta = dt.timedelta(hours = 1.)
    middle = dusk + (end_sunset - dusk) / 2 
    
    ax.text(
        middle - delta, 
        0.5, 
        term_name, 
        transform = ax.transData
        )
    
    delta = dt.timedelta(hours = 8)
    shade_area(
            ax, 
            end_sunset,
            end_sunset + delta, 
            name = midn_name, 
            color = 'lightgray'
            )
    
    delta = dt.timedelta(hours = 0.3)
    ax.text(
        midnight + delta, 
        0.5, 
        midn_name, 
        transform = ax.transData
        )
    delta = dt.timedelta(hours = 2.3)
    ax.text(
        midnight - delta, 
        0.5, 
        'Pré-meia-noite', 
        transform = ax.transData
        )
    
    
    return None 

def plot_epb_time_section(dn):
    
    fig, ax = plt.subplots(
        figsize = (16, 12),
        nrows = 4, 
        sharex = True,
        dpi = 300
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    sectors = list(range(-80, -40, 10))[::-1]
    
    for i, sector in enumerate(sectors):
        
        ax[i].plot(dumb_data(dn))
    
        if i == 0:
            label_top = 1.05
        else:
            label_top = None 
            
        plot_region_shades(
            ax[i], sector, dn, label_top = label_top)
        
        delta = dt.timedelta(hours = 11)
        ax[i].set(
            ylabel = f'Setor {i + 1}',
            xlim = [dn, dn + delta],
            yticklabels = [],
            ylim = [0, 1]
            )
    
    b.format_time_axes(ax[-1], pad = 70)
    
    return fig

def main():
    
    dn = dt.datetime(2013, 12, 24, 21)
    
    fig = plot_epb_time_section(dn)
    
    FigureName = 'time_section_in_sectors'
      
    fig.savefig(
          b.LATEX(FigureName, folder = 'products'),
          dpi = 400
          )