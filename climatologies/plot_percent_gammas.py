import datetime as dt 
import matplotlib.pyplot as plt
import base as b 
import core as c 
import RayleighTaylor as rt 
import pandas as pd 
import numpy as np 
import GEO as gg 

b.config_labels()

args_scatter = dict(s = 30, alpha = 0.4)


def plot_percent_gamma_weigths(
        df, cols, 
        translate = False, 
        freq = '27D'
        ):
    
    fig, ax = plt.subplots(
        figsize = (18, 8), 
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
    
    ds.index = ds.index.map(gg.year_fraction)
    
    names = [ lb.drift, lb.winds, lb.gravity]
    colors = ['red', 'blue',  'k']
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
        0.55, 0.9, 
        sum_label, 
        transform = ax.transAxes
        )
    
    ax.legend(
        ncol = 3, 
        bbox_to_anchor = (0.5, 1.17),
        columnspacing = 0.3,
        loc = "upper center", 
        fontsize = 27
        )
       
    ax.set(
        ylim = [-0.55, 1.2],
        # xlim = [df.index[0], df.index[-1]],
        xticks = np.arange(2013, 2024, 1), 
        xticklabels = np.arange(2013, 2024, 1),
        xlabel = xlabel, 
        ylabel = ylabel
        )
    
    ax.axhline(0, linestyle = '--')
    
    plt.show()
    
    return fig


def main():
    cols = ['gamma', 'drift', 'winds', 'gravity']
    
    df  = c.gamma(
            site = 'saa', 
            time = dt.time(22, 0), 
            el_upper = True,
            file = 'p2',
            gamma_cols = cols
            )
    
    df = df.loc[df.index.year < 2023].dropna()

    fig = plot_percent_gamma_weigths(
        df, cols, translate = False)
        
    FigureName = 'weight_in_each_term'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'climatology'),
        dpi = 300
        )
    
# main()