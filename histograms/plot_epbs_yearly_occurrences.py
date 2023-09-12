import events as ev
import base as b 
import matplotlib.pyplot as plt 
import numpy as np 




def plot_epbs_yearly_occurrence(ds):
    
    fig, ax = plt.subplots(
        figsize = (12, 4), 
        dpi = 300
        )
    
    y = ds['-40'].values
    x = ds.index 
    
    args = dict(facecolor = 'lightgrey', 
                edgecolor = 'black', 
                hatch = '////', 
                color = 'gray', 
                linewidth = 1)
    
    ax.bar(x, y, width = 30, **args)
    
    ax.set(
        xlabel = 'years', 
        ylabel = 'Number of EPBs/month'
        )

ds = b.load('database/epbs/occurrences.txt')

plot_epbs_yearly_occurrence(ds)
