import matplotlib.pyplot as plt
import base as s
import RayleighTaylor as rt
import pandas as pd

s.config_labels()


def plot_parameter(ax, df, col = 'all'):
    epb = df[df['epbs'].isin([1])]
    no_epb = df[df['epbs'].isin([0])]
    
    
    ax.scatter(epb.index, epb[col])
    ax.scatter(no_epb.index, no_epb[col], 
               marker = 'x', color = 'red')

def gamma_annual():

    fig, ax = plt.subplots(
        sharex = True,
        dpi = 300, 
        nrows = 3, 
        figsize = (10, 10), 
        )

    plt.subplots_adjust(hspace = 0.1)
    
    infile = 'database/Results/all_parameters/saa_2013_2015.txt'
    
    df = s.load(infile)
    
    df = df.groupby(df.index).first()
        
    df['all'] = df['all'] * 1e4
  
    
    plot_parameter(ax[0], df, col = 'all')
    lbs = rt.EquationsFT(r = False)

    ax[0].set(ylabel = lbs.label, 
              ylim = [-5, 40])
    
    plot_parameter(ax[1], df, col = 'parl_mer')
    
    ax[1].axhline(0, linestyle = '--')
    ax[1].set(ylabel = '$U^L_{\\parallel}$ (m/s)',
              ylim = [-150, 150])
    
    plot_parameter(ax[2], df, col = 'kp')
    
    ax[2].set(ylim = [0, 9], 
              ylabel = 'Kp', 
              xlim = [df.index[0], df.index[-1]])
    
    s.axes_month_format(ax[2], 
                        month_locator = 4)
    
    


gamma_annual()