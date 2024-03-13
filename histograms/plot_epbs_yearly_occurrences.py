import events as ev
import base as b 
import matplotlib.pyplot as plt 
import numpy as np 
import PlasmaBubbles as pb
import datetime as dt


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

# ds = b.load('database/epbs/occurrences.txt')

# plot_epbs_yearly_occurrence(ds)

s_year = 2012
e_year = 2023


df = b.sel_dates(
    b.load(pb.INDEX_PATH), 
    dt.datetime(s_year, 12, 1), 
    dt.datetime(e_year, 1, 13)
    )


def plot_histogram(ax, arr, binwidth = 10):

    lmax = round(arr.max())
    lmin = round(arr.min())

    bins = np.arange(lmin, 
                     lmax + binwidth, 
                     binwidth)

    ax.set(
           xlim = [lmin - binwidth, 
                   lmax + binwidth]
           )

    args = dict(facecolor = 'lightgrey', 
                alpha = 1, 
                edgecolor = 'black', 
                hatch = '////', 
                color = 'gray', 
                linewidth = 1)


    ax.hist(arr, bins = bins, **args)
         
    return ax
    
fig, ax = plt.subplots(
    figsize = (12, 4), 
    dpi = 300
    )

arr = df['f107'].values
plot_histogram(ax, arr, binwidth = 3)

