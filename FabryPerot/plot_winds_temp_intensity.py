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

def sel_coord(ax, wd, direction, parameter = 'vnu', 
              translate = False):
    
    ds = wd.loc[(wd["dir"] == direction)]
    
    dir_name = {
        'east': 'Leste', 
        'north': 'Norte', 
        'west': 'Oeste', 
        'south': 'Sul'
        }
    
    if translate:
        label = direction
    else:
        label = dir_name[direction]
        
        
    ax.errorbar(
        ds.index, 
        ds[parameter], 
        yerr = ds[f'd{parameter}'], 
        label = label, 
        capsize = 5,
        lw = 2
            )
    
    return None 
        
def title_site(fig, path):    
    if "car" in path:    
        site= "São João do Cariri"
    elif 'bfp' in path:
        site = "Cachoeira Paulista"
    else:
        site = "Cajazeiras"

    fig.suptitle(site)
    
    return None 
    
    
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
    
    return None
    
    
def plot_directions(ax, path, translate = True):
    
    if translate:
        label_temp = "Temperature (K)"
        label_rel = "Relative intensity (R)"
        label_vel = "Velocity (m/s)"
    else:
        label_temp = 'Temperatura (K)'
        label_rel = 'Intensidade (R)' 
        label_vel = 'Velocidade (m/s)'
    
    wd = fp.FPI(path).wind
    tp = fp.FPI(path).temp
    rl = fp.FPI(path).bright
    
    coords = {
        "Zonal": ("east", "west"), 
        "Meridional": ("north", "south")
        }
    
    for col, coord in enumerate(coords.keys()):
                
        for row, direction in enumerate(coords[coord]):
            
            sel_coord(
                ax[0, col], wd, 
                direction, 
                parameter = 'vnu'
                )
            
            sel_coord(
                ax[1, col], tp, 
                direction, 
                parameter = 'tn'
                )
            
            sel_coord(
                ax[2, col], rl, 
                direction, 
                parameter = 'rle'
                )
            
            ax[0, row].axhline(
                0, 
                color = "k", 
                linestyle = "--"
                )
            
            ax[-1, row].axhline(
                0, 
                color = "k", 
                linestyle = "--"
                )
            
        b.format_time_axes(
            ax[-1, col],
            hour_locator = 1, pad = 80)
         
    yticks = np.arange(-200, 400, 100)
    
    ax[0, 0].set(
        ylabel = label_vel, 
        yticks = yticks,
        ylim = [yticks[0] - 50, 
                yticks[-1] + 50]
        )
    
    yticks = np.arange(500, 1400, 200)
    
    ax[1, 0].set(
        ylabel = label_temp, 
        ylim = [yticks[0] - 100,
                yticks[-1] + 100], 
        yticks = yticks
        )
    ax[2, 0].set(
        # ylim = [0, 200],
        ylim = [-2, 2],
        yticks = np.arange(-2, 3, 1),
        ylabel = label_rel) 

    anchor = (0.5, 1.47)
    
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
        figsize = (20, 14), 
        sharex =  'col',
        sharey = 'row',
        dpi = 300
        )
    
    plt.subplots_adjust(
        wspace = 0.05, 
        hspace = 0.1
        )
    
    plot_directions(ax, PATH_FPI, translate = False)
    
    # plot_total_component(ax[0, 0], dn, parameter = 'VN1')
    # plot_total_component(ax[0, 1], dn, parameter = 'VN2')
    
    b.plot_letters(ax, y = 0.85, x = 0.03, fontsize = 40)
    
    title_site(fig, PATH_FPI)
    
    fig.align_ylabels()
    return fig
        

def main():
    
    dn  = dt.datetime(2017, 9, 17)
    
    fig = plot_winds_temp_intensity(dn)
    
    FigureName = dn.strftime('FPI_%Y%m%d')
    
    
  
def main():
        
    PATH_FPI = 'database/FabryPerot/car/minime01_car_20151220.cedar.003.txt'
    # PATH_FPI = 'database/FabryPerot/cj/bfp220724g.7100.txt'
    fig = plot_winds_temp_intensity(PATH_FPI)
    FigureName = 'bfp_20220724'
    fig.savefig(
          b.LATEX(FigureName, folder = 'FPI'),
          dpi = 400
          )


main()