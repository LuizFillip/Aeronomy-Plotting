import matplotlib.pyplot as plt
import pandas as pd
import base as s

def dataset(site = 'saa'):
    
    infile = 'digisonde/data/drift/PRE/saa/'
    
    out = [s.load(infile + f'{year}.txt') 
           for year in range(2013, 2016)]
   
    return pd.concat(out).dropna()
    

def plot_pre_annual_variation():
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (10, 6)
        )
       
    df = dataset()
    ax.scatter(df.index, df['vp'])
    
    
    ax.set(ylabel = "Vertical drift (m/s)", 
           xlim = [df.index[0], df.index[-1]], 
           ylim = [-10, 80])
    
    s.axes_month_format(
            ax, 
            month_locator = 4, 
            pad = 50)
    
    plt.show()
    
    return fig

# f = plot_pre_annual_variation()

    
    
