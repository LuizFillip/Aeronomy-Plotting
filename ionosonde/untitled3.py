# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 19:03:35 2023

@author: Luiz
"""

import matplotlib.pyplot as plt
import numpy as np
import base as b
infile = 'digisonde/data/PRE/jic/2013_2021.txt'
df = b.load(infile)

df = df.loc[~((df['vz'] > 75) )]

fig, ax = plt.subplots(
    figsize = (12, 6), 
                      
    sharex = True, 
    sharey = True)


ax.scatter(df.index, df['vz'])

ax.set(ylim = [-10, 80])