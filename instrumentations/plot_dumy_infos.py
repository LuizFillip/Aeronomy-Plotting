import base as b 
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 
def dumb_data(start):
    
    
    end = start + dt.timedelta(hours = 11)
    time = pd.date_range(start, end, freq = '1min')
    return pd.DataFrame({'Occ': np.zeros(len(time))},
                        index = time)

def layout_with_infos(fontsize = 30):
    
    fig, ax_ion, ax_img,  ax_tec, axes = b.layout4(
          figsize = (12, 20), 
          hspace = 0.3, 
          wspace = 0.3
          )
    
    ax_tec.text(
        0.3, 0.5, 
        'EMBRACE TEC maps', 
        transform = ax_tec.transAxes
        )
    
    ax_ion.text(
        0.1, 0.5, 
        'Ionosonde DPS-4', 
        transform = ax_ion.transAxes
        )
    
    ax_img.text(
        0.2, 0.5, 
        'Cariri\nAll-Sky imager', 
        transform = ax_img.transAxes
        )
    
    fig.text(
        0.03, 0.23, 'ROTI (TECU/min)', 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.95, 0.26, 'Occurrence', 
        fontsize = fontsize, 
        rotation = 'vertical',
        color = 'b'
        )
    
    for axs in [ax_img, ax_ion, ax_tec]:
        axs.set(xticks = [], yticks = [])
        
    start = dt.datetime(2013, 12, 24, 21)
    
    ds = dumb_data(start)
    for i, axs in enumerate(axes):
        name = f'ROTI timeseries - Sector {i + 1}'
        axs.plot(ds)
        axs.text(0.01, 1.1, name, transform = axs.transAxes)
        
        axs.set(ylim = [0, 1], yticks = [])
        
        if i < 3:
            axs.set(xticks = [])
    b.format_time_axes(axs)
    
    pl.plot_lines( 
            axes, 
            start,  
            plot_term =False,
            y = 1
            )
    
    plt.show()
    
layout_with_infos(fontsize = 30)