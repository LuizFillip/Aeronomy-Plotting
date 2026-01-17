import plotting as pl 
import matplotlib.pyplot as plt
import numpy as np
import core as c 
import base as b 
import pandas as pd 
import matplotlib.gridspec as gridspec

b.sci_format(fontsize = 25)



def setdata():
    df = c.category_and_low_indices()
    
    df['year'] = df.index.year
    
    ds = df.groupby(
        ['category','year']
        ).size().unstack(fill_value = 0)
    
    ds = ds.T[['intense', 'moderate', 'weak', 'quiet']]
    
    return ds  

def plot_bars_stacked(ax):
    
    df = setdata()

    colors = {
        'intense': '#8B0000',   # vermelho escuro
        'moderate': '#FF4500',  # laranja forte
        'weak': '#FFD700',      # dourado
        'quiet': '#32CD32'      # verde
    }
    
 
    bottom = np.zeros(len(df))
    for i,  (label, color) in enumerate(colors.items()):
        col = df.columns[i]
        ax.bar(
            df.index, df[col],
            bottom = bottom,
            color = color, 
            label = label, 
            width = 0.5
            )
        
        bottom += df[col].values
    

    for x, total in zip(df.index, bottom):
        ax.text(
            x, total + 0.5, f"{x}",
            ha = "center", 
            va = "bottom",
            fontsize = 20, 
            rotation = 0
        )
        
    ax.set(
        ylim = [0, 30], 
        ylabel = 'Number of cases'
        )
    
    plt.xticks(rotation = 0)
    
    pl.legend_for_sym_h(
        ax, quiet = True, ncol = 2, loc = 'upper center'
        )
    
    return None 


def plot_contour_roti(ax):
    df = b.load('maximums_roti')
    df['date'] = pd.to_datetime(df['date'])
   
    ds = df.pivot(
        index = 'time', 
         columns = 'date', 
         values = '-50'
         ) 
      
    img = ax.contourf(
        ds.columns, 
        ds.index, 
        ds.values,
        levels = np.arange(0, 3.5, 0.2), 
        cmap = 'rainbow'
        )
    
    ax.set(
        ylabel = 'Universal Time', 
        xlim = [df['date'].min(), df['date'].max()]
        )
    
    ticks = np.arange(0, 3.5, 0.5)
    
    cax = ax.inset_axes([1.05, 0., 0.03, 1])

    cb = plt.colorbar(
        img, 
        cax = cax,
        ticks = ticks, 
        location='right'
        )
     
    cb.set_label('ROTI (TECU/min)')
    
    ds = b.load('core/src/geomag/data/stormsphase')
    
    ax.scatter(
        ds.index, 
        np.ones(len(ds)) * 22, color = 'white'
        )
    

    return None 
def plot_indices(ax):
    ds = c.low_omni()
  
    ax.plot(ds['f10.7'])
    
    ax.set(
        ylabel = 'F10.7 (Sfu)', 
        xlabel = 'Years'
        )
    return None 
    
def plot_longterm_occurrences():
    
    fig = plt.figure(
        figsize = (14, 12),
        dpi = 300
        )
    gs = gridspec.GridSpec(3, 1, height_ratios=[1, 1, 1])
    plt.subplots_adjust(hspace = 0.1)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    ax3 = fig.add_subplot(gs[2], sharex=ax2)
    
    ax1.tick_params(labelbottom=False)
    ax2.tick_params(labelbottom=False)
    
    plot_indices(ax3)
    
    plot_contour_roti(ax2)
       
    plot_bars_stacked(ax1)
    
    fig.align_ylabels()
    
    axs = [ax1, ax2, ax3]
    
    b.plot_letters(
            axs, 
            x = 0.02, 
            y = 0.85, 
            offset = 0, 
            fontsize = 30,
            num2white = None
            )

    return fig 


def main():
    fig = plot_longterm_occurrences()
    
    
    pl.savefig(fig, 'long_term_counts')
    
# main()
    
