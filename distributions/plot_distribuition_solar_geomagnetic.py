import numpy as np
import matplotlib.pyplot as plt
import base as b
import events as ev 
from plotting import plot_distribution

df = ev.concat_results('saa')

col = ''
if col == 'gamma':
    vmin, vmax, step = 0, 4, 0.2
    
elif col == 'vp':
    vmin, vmax, step = 0, 85, 5
else:
    vmin, vmax, step = 0, 1, 0.05

all_events = []

level = 100

name = [
    '$F_{10.7} < $' + f' {level}',
    '$F_{10.7} > $' + f' {level}'
    ]

solar_dfs =  ev.solar_levels(
    df, 
    level,
    flux_col = 'f107a'
    )

fig, ax = plt.subplots(
    dpi = 300, 
    sharex = True,
    sharey = True,
    nrows = 2,
    figsize = (12, 8)
    )
 

mag_indeces = ['$Kp \\leq 3$',  '$Kp > 3$']


for i, na in enumerate(mag_indeces):
    
    l = b.chars()[i]
    
    ax[i].text(
        0.02, 0.8, f'({l}) {na}',
        transform = ax[i].transAxes
        )