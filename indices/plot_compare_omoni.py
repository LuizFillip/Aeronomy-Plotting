import matplotlib.pyplot as plt
import base as b
import datetime as dt
import numpy as np



fig, ax = plt.subplots(
    dpi = 300,
    figsize = (14, 10), 
    nrows = 2, 
    sharex = True,
    sharey = True
    )


f2 = 'database/indices/omni.txt'

df = b.load(f2)

col = 'f107a'
df[col].plot(ax = ax[0])


f1 = 'database/indices/omni_pro.txt'

df = b.load(f1)

df[col].plot(ax = ax[1])

ax[1].set(xlim = [df.index[0], df.index[-1]])