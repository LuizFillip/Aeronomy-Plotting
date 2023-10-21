import base as b 
import matplotlib.pyplot as plt 
import events as ev
from plotting import plot_distribution
import numpy as np 


def plot_distributions_seasons(
        df, 
        level = 100, 
        fontsize = 25
        ):
    

    fig, ax = plt.subplots(
        ncols = 2,
        nrows = 2, 
        figsize = (15, 8), 
        sharex = True, 
        sharey = True, 
        dpi = 300
        )
    
    ks = {
         
         3:  'march equinox',
         6:  'june solstice',
         9:  'setember equinox',
         12: 'december solstice'
         }
    
    plt.subplots_adjust(
        hspace = 0.05, wspace = 0.02)
    
    epb_events = []
    for j, ax in enumerate(ax.flat):
        
        month = (j + 1) * 3
        
        season_name = ks[month]
        
        
        name = [
            '$F_{10.7} < $' + f' {level}',
            '$F_{10.7} > $' + f' {level}'
            ]
        
        solar_dfs =  ev.medium_solar_level(df, level)
        
        c_event = []
        total = []
        
        
        for i, l in enumerate(solar_dfs):
            
            index = i + 1
            ds = ev.seasons(l, month)
    
            c = plot_distribution(
                    ax, 
                    ds, 
                    f'({index}) {name[i]}'
                    )
            
            total.append(c)
            
            c_event.append(f'({index}) {c} events')
        
        infos = ('EPB occurrence\n' + 
                 '\n'.join(c_event))
            
        ax.text(
                0.65, 0.15, 
                infos, 
                transform = ax.transAxes
                )
        
        l = b.chars()[j]
        
        epb_events.extend(total)
        ax.text(
            0.03, 0.85,
            f'({l}) {season_name} ({sum(total)} events)',
            transform = ax.transAxes
            )
        
        ax.set(
            ylim = [-0.2, 1.4], 
            yticks = np.arange(0, 1.2, 0.25)
            )
 
    
    ax.legend(
        ncol = 2, 
        bbox_to_anchor = (-.01, 2.3),
        loc = "upper center"
        )
    
    
    fig.text(
        0.05, 0.3, 
        "EPB occurrence probability", 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.45, 0.05, 
        b.y_label('gamma'), 
        fontsize = fontsize
        )
    
    
    fig.suptitle(
        df.columns.name +
        f' ({sum(epb_events)} EPBs events)',
        y = 1.
        )
    
    return fig
    
# def main():

df = ev.concat_results('saa', col_g = 'e_f')

df['doy'] = df.index.day_of_year.copy()

fig = plot_distributions_seasons(df)

