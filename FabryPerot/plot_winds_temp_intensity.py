import matplotlib.pyplot as plt
import FabryPerot as fp
import base as b
import datetime as dt
import numpy as np
import pandas as pd 



b.config_labels()

PATH_FPI = 'database/FabryPerot/'

def get_dn(wd):
    return dt.datetime(
        wd.index[0].year, 
        wd.index[0].month, 
        wd.index[0].day, 21, 0)

def plot_coord(
        ax, 
        wd, 
        direction, 
        parameter = 'vnu', 
        translate = False
        ):
    
    ds = wd.loc[(wd["dir"] == direction)]
    
    dir_name = {
        'east': 'Leste', 
        'north': 'Norte', 
        'west': 'Oeste', 
        'south': 'Sul'
        }
    
    if translate:
        label = direction.title()
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
    
    ax.axhline(
        0, 
        color = "k", 
        linestyle = "--"
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
    
def load_month_avgs():
    
    df = b.load('FabryPerot/data/201512')

    df['time'] = df.index.to_series().apply(b.dn2float)
    df['day'] = df.index.day
    return df.loc[~df.index.duplicated()]



def get_mean_std(df, vl, coord):
    
    co = coord[:5].lower()
    
    ds = pd.pivot_table(
        df, 
        values = f'{vl}_{co}', 
        columns ='day', 
        index = 'time'
        )
    
    ds = pd.concat(
        [ds.mean(axis = 1).to_frame('mean'), 
         ds.std(axis = 1).to_frame('std')],
        axis = 1)
    
    
    dn = dt.datetime(2015, 12, 20)
    
    return b.renew_index_from_date(ds, dn)


def plot_avg(ax, avg, vl, coord):
    
    ds = get_mean_std(avg, vl, coord)

    ds1 = ds.resample('1H').asfreq()

    ax.errorbar(
        x = ds1.index, 
        y = ds1['mean'], 
        yerr = ds1['std'], 
        capsize = 5, 
        marker = 'o',
        markersize = 10, 
        lw = 2,
        color = 'magenta', 
        fillstyle = 'none'
        )
    
    return None 

    
def plot_directions(
        ax, 
        path, 
        translate = True, 
        site = 'bfp'
        ):
    
    if translate:
        label_temp = "Temperature (K)"
        label_rel = "Relative \n intensity (R)"
        label_vel = "Velocity (m/s)"
    else:
        label_temp = 'Temperatura (K)'
        label_rel = 'Intensidade (R)' 
        label_vel = 'Velocidade (m/s)'
    
    fpi = fp.FPI(path)
    
    avg =  load_month_avgs()

   
    coords = {
        "Zonal": ("east", "west"), 
        "Meridional": ("north", "south")
        }
           
    for i, vl in enumerate(['vnu', 'tn', 'rle']):
        
        plot_avg(ax[i, 0], avg, vl, 'zonal')
        plot_avg(ax[i, 1], avg, vl, 'merid')

    
    for col, coord in enumerate(coords.keys()):
                
        for row, direction in enumerate(coords[coord]):
            
            for i, (vl, df) in enumerate(fpi.zips):

                plot_coord(
                    ax[i, col], 
                    df, 
                    direction, 
                    parameter = vl, 
                    translate = translate
                    )
        
                
        b.format_time_axes(
            ax[-1, col], 
            translate = translate,
            hour_locator = 2, 
            pad = 85
            )
        

    ax[0, 0].set(
        ylabel = label_vel, 
        ylim = [-200, 200],
        yticks = np.arange(-200, 300, 100),
        )
        
    ax[1, 0].set(
        ylabel = label_temp, 
        ylim = [500, 1500], 
        yticks = np.arange(500, 1500, 300)
        )
   
    ax[2, 0].set(
        ylim = [-2, 2],
        yticks = np.arange(-2, 3, 1),
        ylabel = label_rel
        ) 

    anchor = (0.5, 1.49)
    
    ax[0, 0].legend(
         ncol = 2, 
         title = 'Zonal',
         loc = 'upper center', 
         bbox_to_anchor = anchor,
         columnspacing = 0.3
         )
    
    ax[0, 1].legend(
         ncol = 2, 
         title = 'Meridional',
         loc = 'upper center', 
         bbox_to_anchor = anchor,
         columnspacing = 0.3
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
    
    plot_directions(ax, PATH_FPI, translate = True)
    
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
    # PATH_FPI = 'database/FabryPerot/cj/bfp240924g.7100.txt'
    fig = plot_winds_temp_intensity(PATH_FPI)
    FigureName = 'FPI_mesuraments'
    path_to_save = 'G:\\My Drive\\Papers\\Paper 2\\Geomagnetic control on EPBs\\June-2024-latex-templates\\'
    
    
    # fig.savefig(path_to_save + FigureName, dpi = 400)


main()


    
    
    
