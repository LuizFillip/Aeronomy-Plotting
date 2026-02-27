import base as b

import core as c 
import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib.gridspec as gridspec




def plot_f107(ax, color = 'magenta'):
    
    ds = c.low_omni()
     
    ds["f107a"] = ds["f10.7"].rolling(window = 81).mean()
     
    ds.index = ds.index.year + (ds.index.day_of_year / 366 )
  
    ax1 = ax.twinx()
    
    ax1.plot(
        ds['f10.7'],
        lw = 1, 
        color = 'w'
        )
    
    ax1.set(    
            yticks = np.arange(0, 400, 100),
            ylim = [60, 900], 
            )
    
    ax1.text(
        1.05, 0, 'F10.7 (sfu)', 
        fontsize = 15, 
        rotation = 'vertical',
        transform = ax1.transAxes
        )
    return 



def plot_contour_roti(ax, start, end, vmax = 3):
 
    df = c.load_averages(start, end)
 
    img = ax.pcolormesh(
        df.columns, 
        df.index, 
        df.values ,
        vmin = 0, 
        vmax = vmax, 
        cmap = 'inferno'
        )
    
    ax.set(
        ylim = [19, 30],
        yticks = np.arange(19, 30, 2),
        ylabel = 'Universal Time'
        )
    
    ticks = np.arange(0, vmax + 1, 0.5)
    
    cax = ax.inset_axes([0.25, 1.25, 0.5, 0.08])

    cb = plt.colorbar(
        img, 
        orientation = 'horizontal',
        cax = cax,
        ticks = ticks 
        )
     
    cb.set_label('ROTI (TECU/min)')
 
    for dn in np.arange(start, end + 1):
        ax.axvline(
            dn, 
            lw = 1, 
            color = 'w', 
            linestyle = '--'
            )
    
    plot_f107(ax, color = 'w')
    
    return None 
    

def plot_equinox_asymetry(
        ax, 
        start, end, 
        percent = True, 
        bar_width = 0.2,
        ylim = [0, 60]
        ):
    
    ds = c.data_epbs(start, end, percent = percent)
    
    lbs = {'march': "black", 'september':  "purple"}
    
    for idx, (name, color) in enumerate(lbs.items()):
         
        if idx == 0:
            offset = 0
        else:
            offset = (bar_width / idx )
        
        label = f'{name.capitalize()} Equinox'
        ax.bar(
               (ds.index + 0.38) + offset,
               ds[name],
               width=bar_width,
               color= color,
               label= label,
               edgecolor = 'k'
           )
            
  
    ax.legend(
        loc = 'upper center',
        ncol = 2,  
        bbox_to_anchor = (0.5, 1.2)
        )
   
    xticks = np.arange(start, end + 1)
    ax.set(
        xlim = [start, end + 1],
        xticks = xticks,
        ylim = ylim,
        yticks = np.arange(0, ylim[-1] + 10, 10),
        ylabel = 'Occurrence rate (\%)', 
        xlabel = 'Years'
           )
    
    for dn in xticks:
        ax.axvline(
            dn, 
            lw = 1, 
            color = 'k', 
            linestyle = '--'
            )
    
    return  None 



def plot_roti_and_bars(
        start = 2010, 
        end = 2023, 
        percent = False
        ):
    
    fig = plt.figure(
        figsize = (12, 8),
        dpi = 300
        )
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])
    plt.subplots_adjust(hspace = 0.2)
    
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex = ax1)
     
    ax1.tick_params(labelbottom=False)
    
    plot_equinox_asymetry(ax2, start, end, percent = percent)
    plot_contour_roti(ax1, start, end)
     
    fig.align_ylabels()
    
    axs = [ax1, ax2]
    
    b.plot_letters(
            axs, 
            x = 0.02, 
            y = 0.8, 
            offset = 0, 
            fontsize = 30,
            num2white = 0
            )
    
    plt.show()
    
    path_to_save = 'G:\\Meu Drive\\Papers\\EquinoxAsymetry\\'
     
    figname = 'roti_and_bars'
    # fig.savefig(path_to_save + figname, dpi = 400)

fig = plot_roti_and_bars(start = 2009, end = 2024)

