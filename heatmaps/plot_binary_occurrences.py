import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import base as b  
import datetime as dt
import pandas as pd

infile = 'D:\\database\\epbs\\events\\2021.txt'


ds = b.load(infile)

dn = dt.datetime(2021, 1, 1, 20)
x = b.sel_times(ds, dn)

fig, ax = plt.subplots()

# define the colors
cmap = mpl.colors.ListedColormap(['w', 'grey'])

# create a normalize object the describes the limits of
# each color
bounds = [0, 0.5, 1]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# plot it
cbar = ax.contourf(
    x.index, 
    x.columns, 
    x.values.T,  
    cmap=cmap, norm=norm) #interpolation='none', aspect = 'auto',

plt.colorbar(cbar)




b.format_time_axes(ax)
