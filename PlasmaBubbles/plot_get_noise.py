# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 13:19:08 2023

@author: Luiz
"""

import GEO as gg
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import PlasmaBubbles as pb 
import datetime as dt
import pandas as pd
import base as b 


            
import GNSS as gs

dn = dt.datetime(2013, 1, 1, 12)
    
path = gs.paths(
    dn.year, 
    dn.timetuple().tm_yday
    ).fn_roti

ds = pb.load_filter(
        path
        )


ds1 = b.sel_times(
    ds, dn, 
    hours = 8
    )

ds1 = pb.longitude_sector(ds1, -70)
fig, ax = plt.subplots()

ax.plot(ds1['roti'])


avg = ds1['roti'].mean()
std = ds1['roti'].std()


ax.axhline(avg , color = 'r')

ax.axhline(avg + std, color = 'b')

ax.set(ylim = [0, 1])

b.format_time_axes(ax)

avg, std