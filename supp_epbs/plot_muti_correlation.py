import base as b
import core as c 
import matplotlib.pyplot as plt 


b.sci_format(fontsize = 25)


def get_sum(df):

    ds = df.groupby(df.index.month).sum()

    for col in ds.columns:
        if col != 'occ':
            ds[col] = ds[col] / ds['occ']
            
    return ds

def get_avg(df):
    
    agg_funcs = {col: 'mean' for col in 
                 df.columns if col != 'occ'}
    agg_funcs['occ'] = 'sum'
    
    return df.groupby(df.index.month).agg(agg_funcs) 


def plot_scatter_and_fit(
        ax, x, y, 
        marker = 's', 
        name = None, 
        dy = 0):
    
    ax.scatter(
        x, y, s = 100, 
        color = 'k', 
        marker = marker, 
        label = name
        )
    
    fit = b.linear_fit(x, y)
    
    corr = fit.r2_score
    
    ax.plot(
        x, fit.y_pred, 
        lw = 2, color = 'r')
    
    ax.text(
        0.02, 0.8 - dy/10, 
        f"r={corr:.2f}", 
        transform = ax.transAxes
        )
    return None 
    


def plot_multi_correlation(df2):
    
    
    fig, ax = plt.subplots(
        ncols = 3, 
        nrows = 2,
        figsize = (14, 10),
        sharey= True,
        dpi = 300
        )
    
    plt.subplots_adjust(
        wspace = 0.1,
        hspace = 0.3
        )
    
    cols = ['bz_mean', 'ae_mean', 
            ['sym_mean', 'sym_min'],
            'speed_mean', 'kp_max', 'f10.7']
    
    # cols = ['sym', 'ae', 'bz']
    
    # names = ['Bz (nT)', 'AE (nT)', 
    #          'SYM-H (nT)', 
    #          '$V_{sw}$ (km/s)', 
    #          'Kp', 'F10.7 (sfu)']
    
    for i, ax in enumerate(ax.flat):
        y = df2['occ'].values
        col = cols[i]
        
        if isinstance(col, list):
            mks = ['s', 'o']
            name = ['Evening', 'Day']
            
            for i, col2 in enumerate(col):
                x = df2[col2].values
                plot_scatter_and_fit(
                    ax, x, y, marker = mks[i], 
                    name = name[i], 
                    dy = i
                    )
                
                ax.set(xlabel = 'SYM-H (nT)')
                
                ax.legend()
        else:
            x = df2[col].values
            plot_scatter_and_fit(ax, x, y)
            
            ax.set(xlabel = cols[i])
        
        if  i == 0 or i == 3:
            
            ax.set(
                ylabel = 'Number of cases', 
                ylim = [0, 30]
                )
            
    return fig 

df =  c.category_and_low_indices(
    col_dst = 'sym_min',
    col_kp = 'kp_max'
    )


df['occ'] = 1


#


# ds
    
def join_mean_and_avents(df):

    df = df.groupby(df.index.month).agg('sum')  
    ds = b.load('core/src/geomag/data/averages')
    
    ds = ds.groupby(ds.index.month).agg('mean')
    
    ds['occ'] = ds.index.map(df['occ'])
    
    return ds.replace(float('nan'), 0)

df = get_sum(df)  

# ds = join_mean_and_avents(df)

fig = plot_multi_correlation(df)


