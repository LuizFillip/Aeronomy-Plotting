import pandas as pd 
import matplotlib.pyplot as plt
import base as b 
from scipy.ndimage import gaussian_filter
 


seasons = {
    "December": [12, 1, 2],
    "March": [3, 4, 5],
    "June": [6, 7, 8],
    "September": [9, 10, 11],
}

def plot_seasonal_occurrence_from_nl(nl, step=2.0):
    
    fig, ax = plt.subplots(
        dpi=300, 
        ncols=4, 
        nrows=1, 
        figsize=(16, 10),
        subplot_kw={"projection": ccrs.PlateCarree()},
    )
    plt.subplots_adjust(wspace=0.02, hspace=0.12)

    axes = ax.flat 
    lat_min = np.round(nl['lat_min'].min())
    lon_min = np.round(nl['lon_min'].min())
    lon_max = np.round(nl['lon_max'].max())
    lat_max = np.round(nl['lat_max'].max())
    
    
    lon_bins = np.arange(lon_min, lon_max + step, step)
    lat_bins = np.arange(lat_min, lat_max + step, step)
    
    for i, (name, months) in enumerate(seasons.items()):
        nl_season = nl.loc[nl.index.month.isin(months)]
        
        grid = occurrence_area_weighted(
            nl_season, lon_bins, lat_bins)
        
        img = plot_map_occ(axes[i], grid)

        l = b.chars()[i]
        axes[i].set_title(f"({l}) {name}", fontsize=28)

        if i != 0:
            axes[i].set(
                xticklabels=[], 
                xlabel="", 
                ylabel="", 
                yticklabels=[]
                )
            
    anchor = [0.3, 0.78, 0.4, 0.025]
    cax = plt.axes(anchor)
    cbar = fig.colorbar(
        img, ax=ax.ravel().tolist(), 
        orientation = "horizontal",
        cax = cax,
        )

    cbar.set_label("Convection activity (\%)", fontsize=22)
    
    # fig.suptitle(str(year), y=0.98, fontsize=28)
    return fig

def limits(df, 
           x0 = -80, x1 = -40, 
           y0 = -10, y1 = 0):
    return  df.loc[
        ((df['Lon'] > x0) & (df['Lon'] < x1)) |
        ((df['Lat'] > y0) & (df['Lat'] < y1))
        ]

x0 = -80
x1 = -40
y0 = -10
y1 = 0


def load_nucleos(year = 2019, sample = '15D'):
    infile = f'GOES/data/nucleos/{year}'
    
    df = b.load(infile)
    
    df['Lon'] = (df['x1'] + df['x0']) / 2
    df['Lat'] = (df['y1'] + df['y0']) / 2
    
    df = limits(df, x0, x1, y0, y1)
    
    df = df.resample(sample).size()
    
    df = (df / df.values.max()) * 100
    
    return df 


def plot_seasonal(df, ds, title):

    fig, ax = plt.subplots(
          dpi = 300, 
          figsize = (16, 8 )
          )
        
    sdf = gaussian_filter(df, sigma=1)

    ax.plot(
        df.index,
        sdf, 
        lw = 3, color = 'blue'
        )
    
    ax.set(
        ylim = [30, 100], 
        ylabel = 'Convective activity (\%)',
        xlabel = 'Years'
        )
    
    b.change_axes_color(
            ax, 
            color = 'blue',
            axis = "y", 
            position = "left"
            )
    
    ax1 = ax.twinx()
    sds = gaussian_filter(ds, sigma=1)
    
    ax1.plot(ds.index, sds,  lw = 3, color = 'red')
    
    io = f' Lat = {y0} - {y1}, Lon = {x0} - {x1}'
    
    ax1.set(
        title = title.title() + io,
        ylabel = 'GW potential energy (J/Kg)', 
        xlabel = 'Years'
        )
    
    b.change_axes_color(
            ax1, 
            color = 'red',
            axis = "y", 
            position = "right"
            )
    
    return fig


 