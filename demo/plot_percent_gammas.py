import pandas as pd
import matplotlib.pyplot as plt
import settings as s
from common import load_by_alt_time
import RayleighTaylor as rt

def plot_percent_gamma_weigths(alt = 300):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        ncols = 3,
        nrows = 3,
        sharey = True, 
        sharex = 'col',
        figsize = (16, 10)
        )
    
    plt.subplots_adjust(
        hspace = 0.3, 
        wspace = 0.05
        )
    
    markers = ['^', 's', 'o']
    
    ft_labels = [
        rt.EquationsFT().gravity(), 
        rt.EquationsFT().winds(), 
        rt.EquationsFT().drift()
        
        ]
    
    rt_labels = [
           rt.EquationsRT().gravity(), 
           rt.EquationsRT().winds(), 
           rt.EquationsRT().drift()
           ]
    
    dates = pd.date_range(
        "2013-3-16 22:00", 
        freq = "1D", 
        periods = 3
        )
    
    names = ['gravity', 'wind', 'drift']
    
    for j, dn in enumerate(dates):
        
        integrated  = rt.gamma_forms(
            load_by_alt_time(
                'total_parameters.txt', alt, dn
                             ), dn, wind = 'mer_ef'
            )   
        
        local = rt.gamma_forms(
            load_by_alt_time(
                'gamma_perp_mer.txt', alt, dn
                             ), dn
            )
        
        mean1 = local.resample('1H').mean()
        mean2 = integrated.resample('1H').mean()
        
        for i, col in enumerate(names):
            
            mean1[col] = mean1[col] / mean1['all']
            mean2[col] = mean2[col] / mean2['all']
            
            ax[i, j].plot(
                mean1[col], 
                marker = markers[i], 
                label = rt_labels[i], 
                )
            
            ax[i, j].plot(
                mean2[col], 
                marker = markers[i], 
                label = ft_labels[i])
            
            ax[i, j].axhline(0.5, linestyle = '--')
            ax[i, j].set( 
                   ylim = [-0.2 , 1.2], 
                   xlim = [local.index[0], 
                           local.index[-1]])
            
            
    
    fig.text(0.07, 0.3, 
             'Relação entre cada termo e o total', 
             rotation = 'vertical', 
             fontsize = 25)
    
    for i in range(3):
        ax[i, 1].legend(
            bbox_to_anchor = (.5, 1.3), 
            ncol = 2, 
            loc = 'upper center')
        s.format_time_axes(ax[2, i], hour_locator = 1)
        
        
    for i, ax in enumerate(ax.flat):
        letter = s.chars()[i]
        ax.text(
            0.04, 0.85, f"({letter})", 
            transform = ax.transAxes
            )
        
    return fig

# fig.savefig('results/figures/relation_gamma.png', dpi = 300)