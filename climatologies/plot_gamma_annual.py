import matplotlib.pyplot as plt
import base as s
import RayleighTaylor as rt
import pandas as pd

s.config_labels()


def plot_parameter(ax, df, col = 'all'):
    epb = df[df['epbs'].isin([1])]
    no_epb = df[df['epbs'].isin([0])]
    
    
    ax.scatter(epb.index, epb[col], label = 'EPBs')
    ax.scatter(no_epb.index, no_epb[col], 
               label = 'No EPBs',
               marker = 'x', color = 'red')

def gamma_annual():

    fig, ax = plt.subplots(
        sharex = True,
        dpi = 300, 
        nrows = 4, 
        figsize = (10, 10), 
        )

    plt.subplots_adjust(hspace = 0.1)
    
    infile = 'database/Results/gamma/saa.txt'
    
    df = s.load(infile)
    
    # df = df.groupby(df.index).first()
        
    # df['all'] = df['all'] * 1e4
  
    
    plot_parameter(ax[0], df, col = 'all')
    lbs = rt.EquationsFT(r = False)

    ax[0].set(ylabel = lbs.label, 
              ylim = [-5, 40])
    
    plot_parameter(ax[1], df, col = 'parl_mer')
    
    ax[1].axhline(0, linestyle = '--')
    ax[1].set(ylabel = '$U^L_{\\parallel}$ (m/s)',
              ylim = [-150, 150])
    
    plot_parameter(ax[2], df, col = 'kp')
    
    ax[2].set(ylim = [0, 10], 
              ylabel = 'Kp', 
              xlim = [df.index[0], df.index[-1]])
    
    s.axes_month_format(ax[3], 
                        month_locator = 4)
        
    plot_parameter(ax[3], df, col = 'vp')
    
    ax[3].set(ylim = [-10, 90], 
              ylabel = '$V_{zp}$ (m/s)')
    ax[0].legend(ncol = 2, 
                 bbox_to_anchor = (0.5, 1.3),
                 loc = 'upper center')
    

from RayleighTaylor import EquationsFT


def main():

    fig, ax = plt.subplots(
        sharex = True,
        sharey = True,
        dpi = 300, 
        figsize = (10, 5), 
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    infile = 'all_results.txt'
    
    df = s.load(infile)
    df = df.loc[~(df['all']> 3.5)]
    
    
    df['gravity'] = df['gravity'] * 1e3
    
    df['winds'] = df['winds']  * 1e3
    
    lb = EquationsFT()
    cols = ['gravity', 'winds', 'all']
    lbs = [lb.gravity, lb.winds, lb.complete]
    for i, col in enumerate(cols):
        
        ax.plot(df[col], label = lbs[i])
    
    ax.set(
        ylabel = '$\\gamma_{FT} ~(\\times 10^{-3}~s^{-1})$', 
        xlabel = 'years'
        )
    
    ax.legend(ncol = 1, 
              bbox_to_anchor = (.5, 1.55),
              loc = "upper center")
    
main()