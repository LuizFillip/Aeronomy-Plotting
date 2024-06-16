import matplotlib.pyplot as plt
import FabryPerot as fp
import base as b
import datetime as dt
import numpy as np
b.config_labels()

PATH_FPI = 'database/FabryPerot/'

def get_dn(wd):
    return dt.datetime(
        wd.index[0].year, 
        wd.index[0].month, 
        wd.index[0].day, 21, 0)

def sel_coord(ax, wd, direction, parameter = 'vnu'):
    
    ds = wd.loc[(wd["dir"] == direction)]
    
    ax.errorbar(
        ds.index, 
        ds[parameter], 
        yerr = ds[f'd{parameter}'], 
        label = f'{direction} (LOS)', 
        capsize = 5,
        lw = 2
            )
        
def title_site(fig, path):    
    if "car" in path:    
        site= "Cariri"
    elif 'bfp' in path:
        site = "Cachoeira Paulista"
    else:
        site = "Cajazeiras"

    fig.suptitle(site)
    
    
def plot_total_component(ax, dn, parameter = 'VN1'):
    file = fp.dn_to_filename(dn, site = 'bfp', code = 7101)
    
    ds = fp.read_file(PATH_FPI + file, drop = True)
    ds = ds.loc[:, [parameter, f'D{parameter}']].dropna()
    ax.errorbar(
        ds.index, 
        ds[parameter], 
        yerr = ds[f'D{parameter}'], 
        capsize = 5,
        lw = 2
            )
    
    
def plot_directions( ax, path):
    
    wd = fp.FPI(path).wind
    tp = fp.FPI(path).temp
    rl = fp.FPI(path).bright
    
    coords = {
        "Zonal": ("east", "west"), 
        "Meridional": ("north", "south")
        }
    
    for col, coord in enumerate(coords.keys()):
                
        for row, direction in enumerate(coords[coord]):
            
            sel_coord(ax[0, col], wd, direction, parameter = 'vnu')
            sel_coord(ax[1, col], tp, direction, parameter = 'tn')
            sel_coord(ax[2, col], rl, direction, parameter = 'rle')
            
            ax[0, row].axhline(0, color = "k", linestyle = "--")
            
        b.format_time_axes(ax[-1, col])
         
    yticks = np.arange(-100, 400, 100)
    ax[0, 0].set(
        ylabel = "Velocity (m/s)", 
        yticks = yticks,
        ylim = [yticks[0], yticks[-1]]
        )
    
    yticks = np.arange(500, 1200, 200)
    ax[1, 0].set(
        ylabel = "Temperature (K)", 
        ylim = [yticks[0], yticks[-1]], 
        yticks = yticks
        )
    ax[2, 0].set(ylabel = "Relative intensity (R)") 

    anchor = (0.5, 1.45)
    ax[0, 0].legend(
         ncol = 2, 
         title = 'Zonal',
         loc = 'upper center', 
         bbox_to_anchor = anchor,
         columnspacing=0.3
         )
    
    ax[0, 1].legend(
         ncol = 2, 
         title = 'Meridional',
         loc = 'upper center', 
         bbox_to_anchor = anchor,
         columnspacing=0.3
         )
    
    return None


def plot_winds_temp_intensity(PATH_FPI):
    
    fig, ax = plt.subplots(
        nrows = 3, 
        ncols = 2,
        figsize = (16, 12), 
        sharex =  'col',
        sharey = 'row',
        dpi = 300
        )
    
    plt.subplots_adjust(
        wspace = 0.02, 
        hspace = 0.05
        )
    
    plot_directions(ax, PATH_FPI)
    
    # plot_total_component(ax[0, 0], dn, parameter = 'VN1')
    # plot_total_component(ax[0, 1], dn, parameter = 'VN2')
    
    b.plot_letters(ax, y = 0.85, x = 0.03)
    
    # title_site(fig, file)
    return fig
        

def main():
    
    dn  = dt.datetime(2017, 9, 17)
    
    fig = plot_winds_temp_intensity(dn)
    
    FigureName = dn.strftime('FPI_%Y%m%d')
    
    
  
def main():
        
    PATH_FPI = 'database/FabryPerot/car/minime01_car_20170917.cedar.txt'
    
    fig = plot_winds_temp_intensity(PATH_FPI)
    FigureName = 'car_20170917'
    fig.savefig(
          b.LATEX(FigureName, folder = 'paper2'),
          dpi = 400
          )
