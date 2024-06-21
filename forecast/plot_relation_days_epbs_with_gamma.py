import matplotlib.pyplot as plt
import base as b 
from matplotlib.legend_handler import HandlerTuple
import numpy as np 
import core as c 


b.config_labels()

names = ['march', 'june', 'september', 'december']

def plot_seasonal_gamma_relation(epb, day):
    

    c = ['k',  '#00B945', '#FF9500', 
         '#FF2C00', '#845B97'] 
    
    
    fig, ax = plt.subplots(
        figsize = (12, 8),
        nrows = 2,
        sharex = True,
        dpi = 300)
    
    plt.subplots_adjust(hspace=0.08)
    
    list_lines = []
    labels = ['Março', 'Junho', 'Setembro', 'Dezembro']
    for i, season in enumerate(names):
    
        line1, = ax[0].plot(
            day[season], 
            color = c[i], 
            lw = 2,
            label = labels[i], 
            marker = 's'
            )
        
        
        line2, = ax[1].plot(
            epb[season],
            lw = 2,
            color = c[i],
            marker = 's',
            )
        
        list_lines.append((line1, line2))
    
        ax[1].set(
            ylabel = '$N_{EPBs}$',
            ylim = [0, 100], 
            xlabel = '$\gamma_{RT}~(10^{-3}~s^{-1})$')
        
        ax[0].set(
           xticks = np.arange(-0.2, 2.6, 0.2),
           ylim = [0, 300],
           ylabel = '$N_{dias}$'
           )
    
    ax[0].legend(
        ncol = 4, 
           columnspacing = 0.4,
           bbox_to_anchor = (0.5, 1.25),
           loc = 'upper center',
        )
    
    b.plot_letters(ax, y = 0.85, x = 0.03)
    
    return fig


df = c.load_results('saa', eyear = 2022)
level = c.limits_on_parts(df['f107a'], parts = 2 )
df_index = c.DisturbedLevels(df)
 
solar_cycles = df_index.F107(level)

ds = solar_cycles[0]

day = c.concat_season_probability(ds, specify = 'days')
epb = c.concat_season_probability(ds, specify = 'epbs')

fig = plot_seasonal_gamma_relation(epb, day)