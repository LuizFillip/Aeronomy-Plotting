import base as b
import core as c 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd 
import plotting as pl 
b.sci_format(fontsize = 20)


def get_sum(df, dist = 'month'):
    
    if dist == 'month':
        ds = df.groupby(df.index.month).sum()
    else:
        ds = df.groupby(df.index.year).sum()
        
    # for col in ds.columns:
    #     if col != 'occ':
    #         ds[col] = ds[col] # / 12
            
    return join_std(ds, dist)

def join_std(df, dist = 'year'):
     infile = 'core/src/geomag/data/2_hours_results_std'
    
     ds = get_avg(b.load(infile), dist)
     
     ds.columns = [f'{c}_std' for c in ds.columns]
    
     return pd.concat([ds, df], axis = 1)


def get_avg(df, dist = 'month'):
    
    if dist == 'month':
        ds = df.groupby(df.index.month).sum()
    else:
        ds = df.groupby(df.index.year).sum()
        
    return ds


def plot_scatter_and_fit(
        ax, x, y, xerr,
        marker = 's', 
        label = '', 
        dy = 0, 
        color = 'red'
        ):
    
    ax.plot(
        x, y, 
        markersize = 10, 
        linestyle = 'none',
        color = color, 
        marker = marker, 
        label = label, 
        alpha = 0.7, 
        # edgecolors= 'k',
        )
    
    fit = b.linear_fit(x, y)
    
    corr = fit.r2_score
    
    ax.plot(
        x, fit.y_pred, 
        lw = 2, color = color)
    
    ax.text(
        0.6, 0.9 - dy/10, 
        f"$R^2$={corr:.2f}", 
        transform = ax.transAxes, 
        color = color
        )
    return None 
    
    
def join_mean_and_avents(df):

    df = df.groupby(df.index.month).agg('sum')  
    ds = b.load('core/src/geomag/data/averages')
    
    ds = ds.groupby(ds.index.month).agg('mean')
    
    ds['occ'] = ds.index.map(df['occ'])
    
    return ds.dropna() #ds.replace(float('nan'), 0)


def plot_multi_correlation(df):
    
    fig, axs = plt.subplots(
        ncols = 3, 
        nrows = 1,
        figsize = (12, 5),
        sharey= True,
        dpi = 300
        )

    plt.subplots_adjust(
        wspace = 0.1,
        hspace = 0.3
        )

    
    df1 = get_sum(df, dist = 'year')  

    df2 = get_sum(df, dist = 'month')  
  
    cols = ['bz_mean', 'ae_mean', 'sym_mean']
    
    mks = ['^', 's']
    colors = ['k', "magenta"]
    xlabel = ['$B_z$ (nT)', 'AE (nT)', 'SYM-H (nT)']
    xlims = [[-30, 30], [-200, 9000], [-1e3, 100]]
    labels = ['Seasonal', 'Solar cycle']
    steps = [10, 3000, 250]
    
    for i, ds in enumerate([df1, df2]):
        
        for j, ax in enumerate(axs.flat):
            c = cols[j]
            y = ds['occ'].values
            x = ds[c].values
            xerr = ds[c + '_std']
            plot_scatter_and_fit(
                ax, x, y, xerr,
                marker = mks[i], 
                label = labels[i],
                dy = i,
                color = colors[i]
                )
            
            ax.set(xlabel = xlabel[j])
            
            xlim = xlims[j]
            step = steps[j]
            
            ax.set(
                ylabel = 'Number of cases', 
                ylim = [0, 30], 
                
                xticks = np.arange(
                    xlim[0], xlim[-1], step
                    ),
                xlim = xlim,
                )
            if j != 0:
                ax.set_ylabel('')
                
    axs[1].set(xlim = [-120, 12000])
    axs[1].legend(
        loc = 'upper center',
        ncol = 2, 
        bbox_to_anchor = (0.5, 1.15)
          )
    b.plot_letters(
            axs, 
            x = 0.04, 
            y = 0.88, 
            offset = 0, 
            fontsize = 25,
            num2white = None
            )
    
    return fig

def main():
    df =  c.category_and_low_indices(
        col_dst = 'sym_min',
        col_kp = 'kp_max'
        )
    
    
    df['occ'] = 1
    
    fig= plot_multi_correlation(df)
    
    pl.savefig(fig, 'correlations')