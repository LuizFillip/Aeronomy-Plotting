import matplotlib.pyplot as plt
import base as s
import RayleighTaylor as rt
import pandas as pd
s.config_labels()


def gamma_annual():

    fig, ax = plt.subplots(
        sharex = True,
        dpi = 300, 
        nrows = 1, 
        figsize = (10, 4), 
        )

    
    
    infile = 'database/Results/all_parameters/saa_2013_2015.txt'
    
    df = s.load(infile)
    
    df = df.groupby(df.index).first()
    df['all'] = df['all'] * 1e4
  
    epb = df[df['epbs'].isin([1])]
    no_epb = df[df['epbs'].isin([0])]
    
    
    ax.scatter(epb.index, epb['all'])
    ax.scatter(no_epb.index, no_epb['all'], 
               marker='x', color = 'red')
    
    lbs = rt.EquationsFT(r = False)
    
    s.axes_month_format(ax, month_locator = 4)
    
    ax.set(ylabel = lbs.label)
    



gamma_annual()