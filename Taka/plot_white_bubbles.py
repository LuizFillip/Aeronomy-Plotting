import pandas as pd 
import matplotlib.pyplot as plt
import base as b 
import numpy as np 


b.sci_format(fontsize = 25)




def set_zonal_drift(infile):
    
    f = open(infile)
    
    lines = f.readlines()
    
    out1 = []
    for ln in lines:
       
        out = []
        for el in ln.split('\t'):
            out.append(
                el.replace('\n', '').strip()
                )
        
        if len(out) > 1:
            out1.append(out)
    
    df = pd.DataFrame(
        out1[1:], 
        columns = out1[0]
        )
    
    df = df.set_index('')
    
    df = df.replace('', float('nan'))
    
    df.index = pd.to_numeric(df.index)
    
   
    return df.astype(float)  

def plot_zonal_drift():
    infile = 'plotting/Taka/data/zonal_drift.txt'
    df = set_zonal_drift(infile)
    df = df.iloc[:-1, :]
    fig, ax = plt.subplots( 
        dpi = 300, 
        figsize = (14, 7)
        )
    
    df = df.drop(columns = ['2022_09_26', '2022_09_27'])
    
    
    for i, col in enumerate(df.columns, 1):
        
        name = col.replace('_', '-')
      
        ax.errorbar(
            df.index, 
            df[col], 
            yerr = df[col]/10, 
            marker = 'o', 
            capsize = 7, 
            lw = 4, 
            label = f'({i}) {name}'
            )
    
    ax.legend(ncol = 3, bbox_to_anchor = (0.5, 1.35), 
              loc = 'upper center')
    
    ax.set(
            xlim = [23, 31], 
           ylim = [-5, 160], 
           yticks = np.arange(0, 180, 20),
           xlabel = 'UT (hrs)', 
           ylabel = 'Zonal speed (m/s)'
           )
    
    ax.axvline(27, color = 'k', linestyle = '--', lw = 3)
    
    b.add_LT_axis(ax, offset_hours=-3, position=-0.18)
    
   
    return fig


def plot_heights():
    
    infile = 'plotting/Taka/data/iono_parameters.txt'
    df = set_zonal_drift(infile)
    
    fig, ax = plt.subplots( 
        dpi = 300, 
        figsize = (14, 7)
        )
    
    for i, col in enumerate(df.columns, 1):
        
        name = col.replace('_', '-')
      
        ax.plot(
            df.index, 
            df[col], 
            lw = 4, 
            label = f'({i}) {name}'
            )
    
    ax.legend(
        ncol = 3, 
              bbox_to_anchor = (0.5, 1.35), 
              loc = 'upper center')
    
    ax.set(
            xlim = [25, 31], 
           ylim = [160, 340], 
           yticks = np.arange(160, 360, 20),
           xlabel = 'UT (hrs)', 
           ylabel = 'h`F (km)'
           )
    
    ax.axvline(27, color = 'k', linestyle = '--', lw = 3)
    
    b.add_LT_axis(ax, offset_hours=-3, position=-0.18)
    
    return fig 

def main():
    fig = plot_heights()
    
    # fig.savefig('heights', dpi = 300)
    
    fig = plot_zonal_drift()
    
    # fig.savefig('zonal_drift', dpi = 300)
    
# main()