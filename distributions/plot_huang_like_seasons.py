import numpy as np
import matplotlib.pyplot as plt
import base as b
import events as ev 
from plotting import plot_distribution

"""
Huanf and Hairston 
We now separate the data into three subsets for three seasons: 
    
    Equinox (March, April, September, October), 
    June solstice (May, June, July, August), 
    December solstice (November, December, January, February)

"""


b.config_labels()

fig, ax = plt.subplots(
    ncols = 2, 
    nrows = 4,
    figsize = (12, 14), 
    dpi = 300, 
    sharex = 'col'
    )


