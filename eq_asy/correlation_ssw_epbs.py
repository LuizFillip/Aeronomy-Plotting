from merra import load_merra 
import pandas as pd 
import numpy as np
import base as b 
import core as c 
import matplotlib.pyplot as plt 
import matplotlib as mpl

b.sci_format(fontsize = 30)

def plot_temperature(ax, start, end, col = 'T_60_90_S'): 
    df = load_merra()
    
    out = []
    for year in range(start, end + 1):
        ds = df.loc[df.index.year == year, col]
        ds.index = ds.index.day_of_year
        
        out.append(ds.to_frame(year))
        
    df = pd.concat(out, axis = 1)  

     
    cols = df.columns.astype(float)
    years = np.array([int(c) for c in cols])
    
    cmap = plt.get_cmap("jet", len(years))
    
    norm = mpl.colors.BoundaryNorm(
        boundaries=np.arange(
            years.min()-0.5, years.max()+1.5),
        ncolors=len(years)
    )
     
    for col, y in zip(df.columns, years):
        ax.plot(
            df.index.values, 
            df[col].values, 
            color = cmap(norm(y)), 
            lw = 3 
            )
    
    ax.plot(df.mean(axis = 1), color = 'k', 
            lw = 4, label = '$T_{avg}$')
    
    ax.legend()
    ax.set(
        ylim = [190, 260], 
        xlabel = 'Day of year', 
        xticks = np.arange(0, 400, 40)
        )
 
    return mpl.cm.ScalarMappable(norm = norm, cmap = cmap)
     


def plot_scatter_fit(
        ax, df, 
        color = 'red', 
        marker = 'o', 
        label  = '', 
        labeled = False
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
        color = 'purple', 
        marker = marker, 
        label = f'{label}', 
        markeredgecolor = 'black',
        markeredgewidth = 3
        )
     
    ax.plot(
        x, fit.y_pred, 
        lw = 3, 
        color = color
        )
    
    ax.set(  xlabel = '$\delta T$ (K)')
    ax.text(
        0.3, 0.85, 
        f"Pearson coeficient = {corr:.2f}", 
        transform = ax.transAxes, 
        color ='k', 
        fontsize = 30
        )
    
    if labeled:
        for year, x, y in zip(df.index, x, y):
            ax.text(x, y + 1, str(year), fontsize=20)

     
    return ax
 

def data_1(start, end, percent = False):
 
    ds = c.data_epbs(
      
        percent = percent, 
        off_time = 0.5, 
        off_shift = 4
        )
    
    ds = c.count_epbs_by_season(
        ds, start, end, percent = percent)

    ds['dev'] = (ds['september'] -  ds['march'])  #/  ds['march']
    
    # ds = ds.loc[(ds.index < 2023) | (ds.index < 2010)]
    
    # print(ds)
      
    return ds 


def data_2(start, end, col = 'T_60_90_S'):
    df = load_merra()
    
    clim = df.groupby(df.index.dayofyear)[col].mean()
     
    df["clim"] = df.index.dayofyear.map(clim)
 
    df['dev'] = (df[col] - df['clim']) 

    df = df.loc[df.index.month.isin([9, 10])]
  
    df = df.groupby(df.index.year).max()
    
    df = df.loc[(df.index >= start) & (df.index <= end)]
    return df

def join(start, end, temp_col, season, percent = False):
   
    y = data_2(start, end, temp_col)
    x = data_1(start, end, percent)
    
    return pd.concat([y[season], x[season]], axis = 1).dropna()




 
def plot_correlation_both_hemispheres( start, end):
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
    # limits = [[-15, 8], [0, 22]]
    for i, hem in enumerate(hemis):
   
        df = join(hem, 'dev')
        
        plot_scatter_fit(
            ax[1, i], df,  
            color = colors[i], 
            label = ''
            )
        
        sm = plot_temperature(ax[0, i], col = hem)
        ax[0, i].set(title = titles[i])
        ax[1, i].set(xlim = [0, 30], ylim = [0, 30])
        
        
    ax[0, 0].set(ylabel = 'Temperature (K)')
    
    cax = ax[0, 1].inset_axes([1.1, 0, 0.05, 1])
    ticks = np.arange(start, end, 2)
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

def plot_correlation_one_hemisphere(
        start, end, hem ='T_60_90_S'):
    
    fig, ax = plt.subplots(
            dpi = 300, 
            nrows = 2,
            figsize = (12, 10)
            )
    
    plt.subplots_adjust(hspace = 0.3)
     
    title = 'Southern Hemisphere (60°-90°, 10hPa)'
    color = 'black'
    df = join(start, end, hem, 'dev')
    plot_scatter_fit(
        ax[1], df,  
        color = color, 
        label = ''
        )
    
    sm = plot_temperature(ax[0], start, end, col = hem)
    ax[0].set(title = title, ylabel = 'Temperature (K)')
    ax[1].set(
        xlim = [-10, 30], ylim = [-10, 30], 
        yticks = np.arange(-10, 40, 10),
        xlabel = '$\Delta T$ (K)', 
        ylabel = '$\Delta$ EPBs'
        )
        
 
    cax = ax[0].inset_axes([1.01, 0, 0.03, 1])
    ticks = np.arange(start, end + 2, 2)
    cb = plt.colorbar(
        sm,  
        cax = cax,
        ticks = ticks 
        )
 
    cb.set_label("Year")
 
   
    
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
    # fig = plot_correlation_both_hemispheres()
    
  
    start, end = 2011, 2021
    
    fig = plot_correlation_one_hemisphere(start, end)
     
    path_to_save = 'G:\\Meu Drive\\Papers\\EquinoxAsymetry\\'
     
    figname = 'correlations_epbs_temperature'
    
    fig.savefig(path_to_save + figname, dpi = 400)
    
    
main()

