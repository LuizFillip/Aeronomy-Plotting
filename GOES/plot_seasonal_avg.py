import base as b

def plot_seasonal_convective_rate(df):
    
    year = df.index[0].year

    months = [
        [12, 1, 2],
        [3, 4, 5], 
        [6, 7, 8],
        [9, 10, 11]
        ]
    
    names = [
        'dez - fev', 
        'mar - mai', 
        'jun - agu',
        'set - nov'
        ]
    
    fig, ax = plt.subplots(
          dpi = 300, 
          ncols = 2, 
          nrows = 2, 
          figsize = (16, 16),
          subplot_kw = 
          {'projection': ccrs.PlateCarree()}
          )
        
    plt.subplots_adjust(wspace = 0., hspace = 0.15)
    
    
    for i, ax in enumerate(ax.flat):
        
        season = months[i]
        ds = set_data(df.loc[df.index.month.isin(season)])
            
        plot_map_contour(ax, ds) 
        
        if i != 2:
            
            ax.set(
                xticklabels = [],
                xlabel = '',
                ylabel = '',
                yticklabels = []
                )
    
        
        ax.set_title(names[i].upper(), fontsize = 30)
        
        
    b.fig_colorbar(
            fig,
            label = 'Occurrence rate of convective nucleos (\%)',
            fontsize = 35,
            vmin = 0, 
            vmax = 100, 
            step = 10,
            orientation = 'horizontal',
            sets = [0.14, 1., 0.75, 0.02] 
            )
    
    fig.suptitle(year, y = 1.1)
    
    return fig
