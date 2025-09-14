import matplotlib.pyplot as plt
import FabryPerot as fp
import base as b
import datetime as dt
import numpy as np

# b.config_labels()

PATH_FPI = 'database/FabryPerot/'
def plot_sky_component(ax, dn, direction, p = 'vnu'):

    wd = fp.FPI(PATH_FPI + fp.fn(dn)).vnu
    
    ds = wd.loc[(wd["dir"] == direction)]
    ds = ds.loc[:, [p, f'd{p}']].dropna()
    ds.index = ds.index.to_series().apply(b.dn2float)
    ds.index = ds.index.where(ds.index >= 20, ds.index + 24)
    ds.loc[ds.index > 30, 'vnu'] = ds['vnu'] + ds['dvnu']
    # print(ds)
    ax.errorbar(
        ds.index, 
        ds[p], 
        yerr = ds[f'd{p}'], 
        capsize = 5,
        lw = 2,
        label = direction + ' (LOS)'
            )
    
    
    ax.axhline(0, linestyle = '--')
    
    return None 

def component_avg(dn):
    
    df = fp.FPI(PATH_FPI + fn(dn)).vnu
    
    df = fp.interpol_directions(
            df, 
            parameter = 'vnu',
            wind_threshold = 400
            )
    
    ds = pd.DataFrame()
    
    ds['mer'] = df[['north', 'south']].mean(axis = 1)
    ds['zon'] = df[['east', 'west']].mean(axis = 1)
    ds['dmer'] = df[['north', 'south']].std(axis = 1)
    ds['dzon'] = df[['east', 'west']].std(axis = 1)
    
    ds.index = ds.index.to_series().apply(b.dn2float)
    
    ds.index = ds.index.where(ds.index >= 20, ds.index + 24)
    return ds


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




def get_dn(wd):
    return dt.datetime(
        wd.index[0].year, 
        wd.index[0].month, 
        wd.index[0].day, 21, 0
        )

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

    fig.suptitle(site, y = 1.)
    
    return None 
    




def plot_avg(ax, coord = 'mer'):
    
    dn = dt.datetime(2015, 12, 20)
    ds = fp.quiettime_winds(coord = coord)
    
    ds = b.renew_index_from_date(ds, dn)

    ds1 = ds.resample('30min').asfreq()

    ax.errorbar(
        x = ds1.index, 
        y = ds1[coord], 
        yerr = ds1['std'], 
        capsize = 5, 
        marker = 'o',
        markersize = 10, 
        lw = 2,
        color = 'magenta', 
        fillstyle = 'none', 
        label = 'Quiettime'
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
    
   
    coords = {
        "Zonal": ("east", "west"), 
        "Meridional": ("north", "south")
        }
           
    plot_avg(ax[0], 'zon')
    plot_avg(ax[1], 'mer')
    
    
    df = fpi.vnu
    
    for col, coord in enumerate(coords.keys()):
        
        l = b.chars()[col]
        
        ax[col].text(
            0.01, 
            0.85, 
            f'({l}) {coord}', 
            transform = ax[col].transAxes
            )      
        
        ax[col].set(
            ylabel = label_vel, 
            ylim = [-200, 200],
            yticks = np.arange(-200, 300, 100),
            )
        
        for row, direction in enumerate(coords[coord]):

            plot_coord(
                ax[col], 
                df, 
                direction, 
                parameter = 'vnu', 
                translate = translate
                )
        
        ax[col].legend(
             ncol = 3, 
             # title = coord,
             loc = 'lower left', 
             # bbox_to_anchor = (0.5, 1.35),
             columnspacing = 0.3
             )
                
        
    


 
        

    return None


def plot_zonal_meridional_winds(PATH_FPI):
    
    fig, ax = plt.subplots(
        nrows = 2, 
        ncols = 1,
        figsize = (16, 12), 
        sharex =  True,
        sharey = True,
        dpi = 300
        )
    
    plt.subplots_adjust(
        wspace = 0.05, 
        hspace = 0.1
        )
    
    plot_directions(ax, PATH_FPI, translate = True)
    
    b.format_time_axes(
        ax[-1], 
        translate = True,
        hour_locator = 1, 
        pad = 85
        )

    title_site(fig, PATH_FPI)
    
    fig.align_ylabels()
    return fig
        

  
def main():
        
    PATH_FPI = 'database/FabryPerot/car/minime01_car_20151220.cedar.003.txt'
   
    fig = plot_zonal_meridional_winds(PATH_FPI)
    FigureName = 'FPI_mesuraments'
    path_to_save = 'G:\\My Drive\\Papers\\Paper 2\\Geomagnetic control on EPBs\\June-2024-latex-templates\\'
    
    
    fig.savefig(path_to_save + FigureName, dpi = 400)


# main()


    

    