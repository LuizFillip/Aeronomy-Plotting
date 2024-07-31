import base as b 
import core as c 
import pandas as pd 
import matplotlib.pyplot as plt 
import datetime as dt 



b.config_labels(fontsize = 30)




def mean_compose(ds, direction = 'zonal'):
    
 
    df1 = pd.pivot_table(
        ds, 
        values = direction, 
        index = 'time', 
        columns = 'day')

    data  = {
        'mean': df1.mean(axis = 1), 
        'std': df1.std(axis = 1), 
        }
    
    df = pd.DataFrame(data, index = df1.index)

    ref = dt.datetime(2014, 1, 1)
    df.index = b.new_index_by_ref(ref, df.index)
    
    return df 

 
def plot_curves(ax, df1, label = ''):
    
    ax.errorbar(
        df1.index, 
        df1['mean'],
        yerr = df1['std'],
        capsize = 5, 
        lw = 1.5,
        marker = 's',
        markersize = 10,
        fillstyle=  'none',
        label = label
        )
    
  
    ax.set(
        ylim = [-50, 150],
        yticks = [0, 50, 100, 150]
        )
    ax.axhline(0, linestyle = ':')
    ax.axhline(100, linestyle = ':')
    b.axes_hour_format(
            ax, 
            hour_locator = 2, 
            )
    
    return None 

def sel_season(df, season):
    
    if season == 'march':
        num = [3, 4]
    elif season == 'september':
        num = [9, 10]
    else:
        num = [12, 11]
        
        
    return df.loc[(df.index.month == num[0]) |
           (df.index.month == num[1])]


def plot_season_zonal_winds(
        axes, 
        col, df, 
        direction = 'zonal',
        # label = 'With EPBs', 
        translate = False, 
        plot_los = False
        ):
    
    seasons = [
        'march', 
        # 'june', 
        'september', 
        'december'
        ]
    
    los = {
        'meridional': ['north', 'south'], 
        'zonal': ['east', 'west']
        }
    for i, season in enumerate(seasons):
        
        # try:
        ds_season = c.SeasonsSplit(
            df, season, 
            translate = translate
            )
        
        ds = sel_season(df, season)
        
        df1 = mean_compose(
            ds,  
            direction = direction
            ).resample('1H').asfreq()
        
            
        plot_curves(axes[i, col], df1)
        
        if plot_los:
            for v in los[direction]:
            
                plot_curves(
                    axes[i, col], 
                    mean_compose(
                        ds,  
                        direction = v
                        ).resample('1H').asfreq()
                    )
            
            
        s = f'{ds_season.name}'
            
        axes[i, col].text(
            0.02, 0.82, s, 
            transform = axes[i, col].transAxes
            
            )
        
        
    l = b.chars()[col]
    
    axes[0, col].text(
        0., 1.1, f'({l})', 
        fontsize = 40,
        transform = axes[0, col].transAxes
        
        )

    return None

    

def set_data(file):
    
    df = b.load('database/FabryPerot/' + file)
    
    df['zonal'] = df[['west', 'east']].mean(axis = 1)
    df['meridional'] = df[['north', 'south']].mean(axis = 1)
    df['time'] = df.index.to_series().apply(b.dn2float)
    df['day'] = (df.index.year + 
                 df.index.month / 12  +
                 df.index.day / 31)
    
    return df

def plot_labels_and_infos(
        fig, 
        direction, 
        translate = True,     
        fontsize = 35
        ):
   
    
    if translate:
        ylabel = f'Velocidade {direction} (m/s)'
        xlabel = 'Hora universal'
    else:
        ylabel = 'Zonal velocity (m/s)'
        xlabel = 'Universal time'
    
    
    fig.text(
          0.04, 0.32, 
          ylabel, 
          fontsize = fontsize, 
          rotation = 'vertical'
          )
    
    fig.text(
          0.44, 0.04, 
          xlabel, 
          fontsize = fontsize, 
          )
    
    return None
    
    
def plot_FPI_seasonal_winds(
        direction = 'zonal',
        translate = False):
    
    fig, ax = plt.subplots(
        nrows = 3,
        ncols = 2,
        sharex = True, 
        sharey = True,
        dpi = 300, 
        figsize = (18, 12)
        )
    
    plt.subplots_adjust(
        hspace = 0.05, 
        wspace = 0.05
        )
    
    df = set_data('mean')
    
    plot_season_zonal_winds(
        ax, 0, df, 
        direction= direction,
        label = '', 
        translate= translate
        )
    
    df = set_data('mean_ch')

    plot_season_zonal_winds(
        ax, 1, df,
        direction= direction,
        label = '', 
        translate= translate
        )
    
    ax[0, 0].set(title = 'São João do Cariri')
    ax[0, 1].set(title =  'Cachoeira Paulista')
    
    
    # ax[0, 0].legend(
    #      ncol = 2, 
    #      loc = 'upper center',
    #      bbox_to_anchor = (1., 1.6),
    #      )
    
    
    plot_labels_and_infos(
            fig, direction, translate = True)
    return fig 

fig = plot_FPI_seasonal_winds(
    direction= 'zonal',
    translate = True
    )



FigureName = 'seasonsal_analysis_'

# fig.savefig(
#     b.LATEX(FigureName, folder = 'FPI'),
#     dpi = 400
#     )

# df = set_data('mean')


# df