import matplotlib.pyplot as plt
import base as b 
import RayleighTaylor as rt
import core as c
import pandas as pd

lb = rt.EquationsFT()

def chars_dataset():

    infile = 'digisonde/data/jic_chars.txt'
    
    return b.load(infile)


def plot_ionosonde_and_models(year = 2015):
    
    fig, ax = plt.subplots(
        nrows = 5,
        figsize = (10, 12), 
        dpi = 300, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
   
    df2 = b.sel_time(chars_dataset(), year)
    df3 = b.sel_time(rt.local_gamma(), year)
    
    df1 = b.sel_time(c.concat_results(site = 'jic'), year)
        
    ax[0].plot(df2['hmF2'], label = 'ionosonde')
    ax[0].plot(df3['hmF2'], label = 'IRI-2016')
    
    ax[1].plot(df2['foF2'], label = 'ionosonde')
    ax[1].plot(df3['foF2'], label = 'IRI-2016')
    
    ax[2].plot(
        df3['gamma'], 
        label = '$(g / \\nu_{in})L^{-1}$'
        )
    ax[2].plot(
        df3['gamma2'],
        label = '$(V_p + g / \\nu_{in}) L^{-1}$'
        )

    ax[3].plot(
        df1['gamma'], label = lb.complete
        )
    
    ax[4].plot(df3['vp'])
    
    names = ['hmF2 (km)', 'foF2 (MHz)',
             '$\\gamma_{RT}~(s^{-1})$', 
             '$\\gamma_{RT}~(s^{-1})$', 
             '$V_p$ (m/s)']
    
    
    for i, ax in enumerate(ax.flat):
        ax.legend(ncol = 2,  loc = 'upper center')
        ax.set(ylabel = names[i], 
               xlim = [df2.index[0], df2.index[-1]])
        
        if i == 4:
            b.format_month_axes(
                    ax, 
                    month_locator = 1)
        if  i == 0:
            ax.set(ylim = [200, 700],
                   title = year)
        elif i == 4:
            ax.set(ylim = [0, 50])
        elif i == 1:
            ax.set(ylim = [0, 20])
        else:
            ax.set(ylim = [-0.5, 3])
            
    return fig
        
        
# fig = plot_ionosonde_and_models(year = 2014)