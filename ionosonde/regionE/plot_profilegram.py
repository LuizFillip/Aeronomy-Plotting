import digisonde as dg 
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 
infile = 'plotting/ionosonde/regionE/profiles'
df = dg.Profilegram(infile) 
df["ne"] = np.log10((1.24e4 * df["freq"]**2) * 1e6)

df['time'] = df.index.hour + df.index.minute/60

df['day'] = df.index.day 

ds = df.copy()
ds = df.loc[df.index.day.isin([13, 16, 18, 29])]


p = 'ne'


# ds = ds.loc[ds.alt == alt]
ds = ds.loc[(ds.day == 16) & (ds.alt < 200)]


fig, ax = plt.subplots(
    nrows = 2, 
    sharey=True, 
    sharex = True
    )

def plot(ax):
    dss = pd.pivot_table(
        ds, 
        columns = 'time',
        index = 'alt', 
        values = p ).interpolate()

    img = ax[0].contourf(
        dss.columns, 
        dss.index, 
        dss.values, 
        cmap = 'jet'
        )

    plt.colorbar(img)
    
    
ds = df.loc[(df.day == 20) & (df.alt < 200)]

dss = pd.pivot_table(ds, columns = 'time', index = 'alt', values = p ).interpolate()

img = ax[1].contourf(
    dss.columns, 
    dss.index, 
    dss.values, 
    cmap = 'jet'
    )
ax[1].set(ylim = [100, 200]) 
# ax.axhline(0)



plt.colorbar(img)