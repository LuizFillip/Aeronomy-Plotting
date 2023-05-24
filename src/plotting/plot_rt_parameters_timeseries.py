# -*- coding: utf-8 -*-
"""
Created on Wed May 24 03:32:37 2023

@author: Luiz
"""

import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from labels import Labels

df = pd.read_csv("gamma_parameters.txt", index_col = 0)
df.index = pd.to_datetime(df.index)

dn = dt.datetime(2013, 9, 20, 20)
alt = 250


df = df.loc[(df["alt"] == alt) & 
            (df.index >= dn) &
            (df.index <= dn + dt.timedelta(seconds = 43200))]

fig, ax = plt.subplots()

lbs = Labels().infos
def plot_ne_L(ax, df):
    ax.plot(df["L"])
    
    ax.set(ylabel = lbs["L"])
    
    ax1 = ax.twinx()
    
    ax1.plot(df["Ne"])
    
    
plot_ne_L(ax, df)