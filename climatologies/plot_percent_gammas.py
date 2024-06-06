import datetime as dt 
import matplotlib.pyplot as plt
import base as b 
import core as c 
import RayleighTaylor as rt 
import pandas as pd 

b.config_labels()

args_scatter = dict(s = 30, alpha = 0.4)


def plot_percent_gamma_weigths(
        df, cols, 
        translate = False, 
        freq = '27D'
        ):
    
    fig, ax = plt.subplots(
        figsize = (16, 8), 
        dpi = 300, 
        sharex = True, 
        nrows = 1
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    if translate:
        ylabel = 'Contribution on $\gamma_{RT}$'
        xlabel = 'Years'
        sum_label = 'Sum of all terms'
    else:
        ylabel = 'Contribuição em $\gamma_{RT}$'
        xlabel = 'Anos'
        sum_label = 'Soma de todos os termos'

    lb = rt.EquationsFT()
   
    ds = df.resample(freq).mean()
    
    names = [lb.winds, lb.drift,  lb.gravity]
    colors = ['blue', 'red', 'green']
    markers = ['^', 's', 'o']
    out = []
    
    for i, col in enumerate(cols[1:]):
        
        percent = (ds[col] / ds['gamma'])
        # ax[0].plot(
        #     ds[col],
        #     label = names[i], 
        #     lw = 1,
        #     marker = markers[i],
        #     color = colors[i]
        #         )
        
        ax.plot(
            percent,
            lw = 1,
            label = names[i],
            marker = markers[i],
            color = colors[i]
                )
        out.append(percent)
        
    su = pd.concat(out, axis = 1).sum(axis = 1).round()
    
    ax.scatter(su.index, su, s = 10, c = 'k')
    
    ax.text(
        0.8, 0.9, 
        sum_label, 
        transform = ax.transAxes
        )
    
    ax.legend(
        ncol = 3, 
        bbox_to_anchor = (0.5, 1.2),
        columnspacing = 0.3,
        loc = "upper center"      
        )
    
   
       
    ax.set(
        ylim = [-0.55, 1.2],
        xlim = [df.index[0], df.index[-1]],
        xlabel = xlabel, 
        ylabel = ylabel
        )
    
    # ax[0].set(
    #     ylabel = lb.ylabel, 
    #     ylim = [-0.5, 3]
    #     )
    
    ax.axhline(0, linestyle = '--')
    
    # b.plot_letters(
    #     ax, 
    #     y = 0.85, 
    #     x = 0.02, 
    #     num2white = None
    #     )
    
    plt.show()
    
    return fig


def main():
    cols = ['gamma',  'winds', 'drift', 'gravity']
    
    df  = c.gamma(
            site = 'saa', 
            time = dt.time(22, 0), 
            el_upper = True,
            file = 'p2',
            gamma_cols = cols
            )
    
    df = df.loc[df.index.year < 2023].dropna()

    fig = plot_percent_gamma_weigths(
        df, cols, translate = True)
        
    FigureName = 'weight_in_each_term'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'climatology'),
        dpi = 300
        )
    
    
# main()