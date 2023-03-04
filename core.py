from FabryPerot.core import load_FPI
from Digisonde.drift import load_DRIFT
import pandas as pd
import datetime as dt
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def func(x, a, c):
    return a * x + c


def get_values(time, coords = ["mer", "vy"], 
               month = 1):

    df = pd.concat([load_FPI(), 
                load_DRIFT()], axis = 1).dropna()

    sel = df.loc[(df.index.time == time) &
                 (df.index.month == month), coords ]
    
    return sel.iloc[:, 0].values, sel.iloc[:, 1].values


def plotScatter(ax, 
                n, 
                time, 
                coords = ["zon", "vx"]):
        
    xdata, ydata =  get_values(time,  
                              coords = coords, 
                              month = n)
    
    
    ax.plot(xdata, ydata, color = "k",
             linestyle = "none", marker = "o")
    
    ax.set(title = f"Mês - {n}")
    
    popt, pcov = curve_fit(func, xdata, ydata)
    
    ax.grid()
    ax.plot(xdata, func(xdata, *popt), 'r-')
    
