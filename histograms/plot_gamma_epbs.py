import events as ev
import base as b 
import matplotlib.pyplot as plt 
import numpy as np 


df = b.load('all_results.txt')

b.config_labels()

args = dict(
     facecolor = 'lightgrey', 
     edgecolor = 'black', 
     hatch = '////', 
     color = 'gray', 
     linewidth = 1
     )

def plot_gamma_epbs_count(df, step = 0.2):
    

    ds = ev.probability_distribuition(
        df,
        step = step, 
        col_gamma = 'all',
        col_epbs = '-40'
        )
    
   
    fig, ax = plt.subplots(
        figsize = (12, 6), 
        dpi = 300
        )
    
    
    ax.bar(
        ds['start'],
        ds['epbs'], 
        width = step, 
        **args)
    
    ax.set(
        xticks = np.arange(0, 4.8, 0.4), 
        xlabel = '$\\gamma_{FT}$ ($\\times 10^{-3} ~s^{-1}$)', 
        ylabel = 'EPBs count'
        )
    
# plot_gamma_epbs_count(df)