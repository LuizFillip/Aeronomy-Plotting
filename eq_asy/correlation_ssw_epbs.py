from merra import load_merra 
import pandas as pd 
import numpy as np
import base as b 
import core as c 
import matplotlib.pyplot as plt 


def plot_temperature(ax, col = 'T_60_90_S'): 
    df = load_merra()
    
    out = []
    for year in range(2009, 2025):
        ds = df.loc[df.index.year == year, col]
        ds.index = ds.index.day_of_year
        
        out.append(ds.to_frame(year))
        
    df = pd.concat(out, axis = 1)  
    
    
    import matplotlib as mpl
     
    cols = df.columns.astype(float)
    years = np.array([int(c) for c in cols])
    
    cmap = plt.get_cmap("jet", len(years))
    
    norm = mpl.colors.BoundaryNorm(
        boundaries=np.arange(years.min()-0.5, years.max()+1.5),
        ncolors=len(years)
    )
     
    for col, y in zip(df.columns, years):
        ax.plot(df.index.values, 
                df[col].values, 
                color=cmap(norm(y)), 
                lw=2)
    
    ax.plot(df.mean(axis = 1), color = 'k', lw = 4)
 
    ax.set(ylim = [180, 280], xlabel = 'Day of year', 
           xticks = np.arange(0, 400, 40)
           )
    
    return mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
     
 #


def plot_scatter_fit(
        ax, df, 
        color = 'red', 
        marker = 's', 
        label  = ''
        ):
 
    x = df.iloc[:, 0].values
    y = df.iloc[:, 1].values
    
    fit = b.linear_fit(x, y)
    
    corr = np.corrcoef(x, y)[1, 0]
    label = label.capitalize()
    ax.plot(
        x, y, 
        markersize = 15, 
        linestyle = 'none',
        color = color, 
        marker = marker, 
        label = f'{label}', 
        markeredgecolor = 'black',
        markeredgewidth = 2
        )
     
    ax.plot(
        x, fit.y_pred, 
        lw = 3, 
        color = color
        )
    
    ax.set(ylim = [-1, 25], 
           xlabel = '$\delta T$ (K)')
    ax.text(
        0.75, 0.85, 
        f"r = {corr:.2f}", 
        transform = ax.transAxes, 
        color ='k', 
        fontsize = 30
        )
    return ax
 

def data_1(start, end, percent = False):
 
    ds = c.data_epbs(start, end, percent = percent)

    ds['dev'] = (ds['september'] -  ds['march'])  
      
    return ds 


def data_2(start, end, col = 'T_60_90_S'):
    df = load_merra()

    ds = c.average_equinox(df[col], start, end) 
    
    ds['dev'] = (ds['september'] -  ds['march'])  
    return ds

def join(tcol, season, percent = False):
    start, end = 2009, 2024
    y = data_2(start, end, tcol)
    x = data_1(start, end, percent)
    
    return pd.concat([y[season], x[season]], axis = 1)  




 
def plot_correlation_both_hemispheres():
    fig, ax = plt.subplots(
            dpi = 300, 
            ncols = 2,
            nrows = 2,
            sharey = 'row',
            figsize = (16, 10)
            )
    
    plt.subplots_adjust(wspace = 0.05)
    
    colors = ['purple', 'purple']
    hemis = ['T_60_90_N', 'T_60_90_S']
    titles = ['Northern Hemisphere (60°-90°, 10hPa)', 
              'Southern Hemisphere (60°-90°, 10hPa)']
    limits = [[-15, 8], [0, 22]]
    for i, hem in enumerate(hemis):
   
        df = join(hem, 'dev')
        plot_scatter_fit(
            ax[1, i], df,  
            color = colors[i], 
            label = ''
            )
        
        sm = plot_temperature(ax[0, i], col = hem)
        ax[0, i].set(title = titles[i])
        ax[1, i].set(xlim = limits[i])
        
        
    ax[0, 0].set(ylabel = 'Temperature (K)')
    
    cax = ax[0, 1].inset_axes([1.1, 0, 0.05, 1])
    ticks = np.arange(2009, 2025, 2)
    cb = plt.colorbar(
        sm,  
        cax = cax,
        ticks = ticks 
        )
 
    cb.set_label("Year")
    
 

    ax[1, 0].set(
     
        xlabel = '$\delta T$ (K)', 
        ylabel = '$\delta_{EPBs} $'
        )
   
    
    fig.align_ylabels()
    
    b.plot_letters(
            ax, 
            x = 0.04, 
            y = 0.85, 
            offset = 0, 
            fontsize = 30,
            num2white = None
            )
    
    return fig 
    
def main():
    fig = plot_correlation_both_hemispheres()
    
    path_to_save = 'G:\\Meu Drive\\Papers\\EquinoxAsymetry\\'
     
    figname = 'correlations_epbs_temperature'
    fig.savefig(path_to_save + figname, dpi = 400)
    
    
# df = join('T_60_90_N', 'dev', True)
# df.columns = ['temp', 'epb']
# df.sort_values(by = 'epb')