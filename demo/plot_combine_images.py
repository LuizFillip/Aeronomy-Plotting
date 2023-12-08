from skimage import io
import os
import matplotlib.pyplot as plt
import GEO as gg 
import cartopy.crs as ccrs


def figure(year = 2014):
    fig, ax = plt.subplots(
        ncols = 3, 
        dpi = 300,
        sharey = True,
        sharex = True,
        figsize = (14, 10),
        subplot_kw={
            'projection': ccrs.PlateCarree()}
        )
    
    plt.subplots_adjust(wspace= 0.1)
    
    for i in range(3):
        gg.map_attrs(ax[i], year, grid = False)
        if i != 0:
            
    

    return fig, ax
        
def run():
    for fn in os.listdir('temp0/'):
        print(fn)
        plt.ioff()
        # fig = combine(fn)
        # fig.savefig(f'temp3/{fn}', dpi = 300)
        plt.clf()   
        plt.close()
    
fig, ax = figure(year = 2014)

plt.show()