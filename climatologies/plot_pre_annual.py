import matplotlib.pyplot as plt
import pandas as pd
import base as s

def dataset(site = 'saa', ys = 2013, ye = 2023):
    
    infile = f'digisonde/data/drift/PRE/{site}/'

    years = list( range(ys, ye))
    
    
    out = []
    for year in years:
        ds = s.load(infile + f'{year}.txt')
        
        
    
   
    return pd.concat(out)
    

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

df = dataset()

df

    
    
