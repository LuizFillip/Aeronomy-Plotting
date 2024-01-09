import os
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt
import GEO as g
import base as b 

fig, ax = plt.subplots(
     figsize = (20, 15), 
     dpi = 300, 
     ncols = 5, 
     nrows = 3,
     subplot_kw = 
     {'projection': ccrs.PlateCarree()}
     )

plt.subplots_adjust(wspace = 0.05, hspace=0.25)
    
delta = dt.timedelta(hours = 4)
