import base as b
import cartopy.crs as ccrs
import datetime as dt
import plotting as pl
import matplotlib.pyplot as plt 

b.sci_format(fontsize = 25)

def add_red_arrows_on_panels(
        axes,  *,
        crs= ccrs.PlateCarree(),         # normais
        dy=3,                
        color="red",
        lw=2.0,
        arrowstyle="-|>"
    ):
    
    import matplotlib.patches as mpatches

    coords = [[(-52, -8), (-44, -8)], [(-60, -5), (-50, -5)]]
    cols = [0, 2]
    for c, items in zip(cols, coords):
        ax = axes[c]
        for item in items:
            x, y = item

            arrow1 = mpatches.FancyArrowPatch(
                (x, y + 10), (x, y),
                mutation_scale=40,
                color="red",
                transform=ax.transData
                )
            
            ax.add_patch(arrow1)
    
    return None 


def plot_alldays_one_time():
    
    fig, axs = plt.subplots(
         figsize = (16, 8), 
         dpi = 300, 
         ncols = 3, 
         subplot_kw = 
         {'projection': ccrs.PlateCarree()}
         )
    
    plt.subplots_adjust(
        wspace = 0.1, 
        hspace = 0.3
        )
    
    vmax = 60
    
    for col, day in enumerate([20, 21, 22]):
        dn = dt.datetime(2015, 12, day, 0, 0)
        
        ax = axs[col]
        
        pl.plot_tec_map(
            dn, 
            ax = ax, 
            vmax = vmax, 
            root = 'E:\\',
            boxes = False,
            colorbar = False
            )
        
        ax.set(title = dn.strftime('%d/%m/%y %H:%M HU'))
        
        if day > 20:
            ax.set(
                ylabel = '',
                yticklabels = [],
                xticklabels = [],
                xlabel = ''
                )
    
    cbar = r'CET ($10^{16} / m^2$)' 
    
    b.fig_colorbar(
             fig,
             vmin = 0, 
             vmax = vmax, 
             step = 10,
             orientation = 'vertical',
             anchor = [.92, 0.26, 0.02, 0.48], 
             label = cbar
             )
    add_red_arrows_on_panels(
        axs,   
        )

    fig.suptitle('Supressão de Bolhas de Plasma Equatoriais durante\n a Tempestade Geomagnética de Dezembro de 2015', y = 0.95)

    return fig 

    
     
def plot_one_day_alltimes():

    
    fig, axs = plt.subplots(
         figsize = (18, 12), 
         dpi = 300, 
         ncols = 4, 
         subplot_kw = 
         {'projection': ccrs.PlateCarree()}
         )
    
    plt.subplots_adjust(
        wspace = 0.1
        )
    
    vmax = 60
    
    for col in range(4):
        delta = dt.timedelta(hours = col)
        
        dn = dt.datetime(2015, 12, 20, 22) + delta
        ax = axs[col]
        
        pl.plot_tec_map(
            dn, 
            ax = ax, 
            vmax = vmax, 
            root = 'E:\\',
            boxes = False,
            colorbar = False
            )
        
        ax.set(title = dn.strftime(f'({col + 1}) %H:%M HU'))
        
        if col > 0:
            ax.set(
                ylabel = '',
                yticklabels = [],
                xticklabels = [],
                xlabel = ''
                )
    
    cbar = r'CET ($10^{16} / m^2$)' 
    
    b.fig_colorbar(
             fig,
             vmin = 0, 
             vmax = vmax, 
             step = 10,
             orientation = 'vertical',
             anchor = [.92, 0.37, 0.02, 0.27], 
             label = cbar
             )
    
    
    
    fig.suptitle('Supressão de Bolhas de Plasma Equatoriais durante\n a Tempestade Geomagnética de 20-21 Dezembro de 2015', y = 0.76)
    
    return fig 


figs = [plot_alldays_one_time(), 
        plot_one_day_alltimes()]

names = ['alldays', 'alltimes']
for i, fig in enumerate(figs):
    
    fig.savefig(names[i], dpi = 400)