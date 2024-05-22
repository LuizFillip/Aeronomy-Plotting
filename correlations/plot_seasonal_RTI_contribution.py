import plotting as pl
import core as c 
import matplotlib.pyplot as plt 
import base as b


b.config_labels()

def plot_seasonal_RTI_contribution(df):
    fig, ax = plt.subplots(
        nrows = 4, 
        ncols = 3, 
        sharey = 'row',
        sharex = 'col',
        dpi = 300,
        figsize = (18, 16)
        )
    
    plt.subplots_adjust(wspace = 0.01)
    
    
    names = ['march', 'june', 'september', 'december']
     
    # b.plot_letters(ax, y = 1.04, x = 0.01)
    
    for i, name in enumerate(names):
            
        ds_split = c.SeasonsSplit(df, name)
                
        pl.plot_single_correlation(
            ds_split.sel_season, 
            ax = ax[i, 0], 
            color = 'k', 
            col = 'vp',
            index = 0, 
            label = ''
            )
        
        pl.plot_single_correlation(
            ds_split.sel_season, 
            ax = ax[i, 1], 
            color = 'k', 
            col = 'K',
            index = 0, 
            label = ''
            )
        
        pl.plot_single_correlation(
            ds_split.sel_season, 
            ax = ax[i, 2], 
            color = 'k', 
            col = 'gr',
            index = 0, 
            label = ''
            )
        
        ax[i, 0].set(
            title = ds_split.name
            )
        ax[i, 1].set(
            title = ds_split.name
            )
        ax[i, 2].set(
            title = ds_split.name
            )
    
    ax[-1, 0].set(xlabel = b.y_label('vp'))
    ax[-1, 1].set(xlabel = b.y_label('K'), xlim = [1, 4.2])
    ax[-1, 2].set(xlabel = b.y_label('g_nui_eff'), xlim = [0, 30])
    
    fontsize = 35
    
    fig.text(
          0.045, 0.4, 
          b.y_label('gamma'), 
          fontsize = fontsize, 
          rotation = 'vertical'
          )
    
    plt.show()
    return fig


fig, ax = plot_seasonal_RTI_contribution()

df = c.load_results('saa', eyear = 2022)

df['K']  = df['K'] *  1e5

fig = plot_seasonal_RTI_contribution(df)