import pandas as pd
import matplotlib.pyplot as plt
import os
from PRE import drift
from core import iono_frame
from utils import smooth
import setup as s
from datetime import timedelta
import numpy as np

df = pd.read_csv("database/drift/016.txt", index_col = 0)
df.index = pd.to_datetime(df.index)
df = df.loc[df.index.hour >= 18]

x = df.index
y = df["17"].values



infile = "database/process/SL_2014-2015/"

_, _, files = next(os.walk(infile))

filename = files[0]


df1 = drift(iono_frame(infile + filename).sel_day_in(day = 16))


def plot():

    fig, ax = plt.subplots(figsize = (10, 4))
    
    
    args = dict(lw = 1.5)
    ax.plot(df1[[6, 7, 8]].mean(axis = 1), 
            color = "k", **args,
            label = "Dados reduzidos (SAO-X)")
    
    ax.plot(x, y, 
            label = "Dados brutos (Drift-X)",
            **args)
    
    ax.plot(x, smooth(y, 3), 'r-', 
            label = "Suavização (30 min)", **args)
    
    s.format_axes_date(ax, time_scale = "hour")
    
    delta = timedelta(minutes = 10)
    ax.grid()
    
    start, end = min(df.index) - delta, max(df.index) + delta
    
    ax.set(ylabel = "$V_z$ (m/s)", 
           xlabel = "Hora universal (UT)", 
           yticks = np.arange(-60, 70, 10),
           ylim = [-60, 60], 
           xlim = [start, end])
    
    ax.legend()
    
plot()