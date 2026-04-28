import matplotlib.pyplot as plt
import plotting as pl 
import digisonde as dg 
import datetime as dt 
import matplotlib.patches as mpatches
import base as b 
import numpy as np 

b.sci_format(fontsize = 25)


def plot_ionogram_examples(
        dates, 
        site = 'SAA0K'
        ):
      
    fig, ax = plt.subplots(
        figsize = (16, 8),
        dpi = 300,
        ncols = len(dates),
        sharex = True,
  
        )
    
    
    plt.subplots_adjust(wspace = 0.05)
    
    ys = [110, 130, 100]
    xs = [9.5, 8.5, 4]
    for i, dn in enumerate(dates):
        fname = dg.IonoDir(
            site, dn, root = 'D').dn2PNG
        
        fname = f'D:\\ionogram\\quiet\\{fname}'
       
        pl.plot_single_ionogram(
            fname, ax = ax[i], label = True)
        
        ax[i].set(
            ylim = [80, 900],
            yticks = np.arange(100, 1000, 100),
            title = dn.strftime('%d/%m/%y %H:%M UT')
            )
        
        x_tail, y_tail = xs[i] + 4, ys[i]
        x_head, y_head = xs[i], ys[i]
        
        arrow1 = mpatches.FancyArrowPatch(
            (x_tail, y_tail), (x_head, y_head),
            mutation_scale = 50,
            color="red",
            transform=ax[i].transData, 
            
            )
        
        ax[i].add_patch(arrow1)
        
        if i != 0:
            ax[i].set(ylabel = '', yticks = [])
            
        l = b.chars()[i]
         
        ax[i].text(
             0.05, 0.87, 
             s = f'({l})',
             fontsize = 30,
             transform = ax[i].transAxes
             , color = 'w'
             )
    
    b.plot_letters(
            ax, 
            x = 0.02, 
            y = 0.8, 
            offset = 0, 
            fontsize = 30,
            num2white = [0, 1, 2]
            )


    return fig
def main():
    
    dates = [
        dt.datetime(2020, 3, 2, 22, 40), 
        dt.datetime(2020, 1, 12, 22, 0),
        dt.datetime(2020, 1, 16, 22, 20)
         ]
    fig = plot_ionogram_examples(dates)
    
    pl.savefig(fig, 'Es_examples')
    
# main()