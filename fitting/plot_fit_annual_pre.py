import matplotlib.pyplot as plt
import numpy as np 
from scipy.optimize import curve_fit
import base as b
import os 


b.config_labels()   
PATH_PRE = 'digisonde/data/PRE/'
def set_data(site = 'saa'):

    infile = os.path.join(
        PATH_PRE, 
        f'{site}/2013_2021.txt'
        )
    
    df = b.load(infile)
    
    df.rename(
        columns = {'vp': 'vz'}, 
        inplace = True
        )
    
    return df 
def func(x, a, b):
    arg = 360 / 365 * (250 + x)
    return a * np.sin(-np.radians(arg)) + b



df = set_data(site = 'jic')
df = df.loc[df.index.year == 2016]
df = df.loc[~((df['vz'] > 30) | 
              (df['vz'] < 0)), ['vz']]




 
df = df.dropna()

df['doy'] = df.index.day_of_year 

xdata = df['doy'].values 
ydata = df['vz'].values


popt, pcov = curve_fit(func, xdata, ydata)

yfit = func(xdata, *popt)
fig, ax = plt.subplots()

ax.scatter(xdata, ydata)
ax.plot(xdata, yfit, 'r-')


# len(yfit), len(df)

