import pandas as pd
import matplotlib.pyplot as plt
from Digisonde.drift_utils import load_drift
import numpy as np
import datetime as dt
from Liken.utils import get_fit2
from sklearn.linear_model import LinearRegression

def plot_data(ax, 
              xdata, ydata):
    ax.plot(xdata, ydata,
            marker = "o", 
            linestyle = "none", 
            color = "k")

    fit, r2 = get_fit2(xdata, ydata)

    ax.plot(xdata, fit, 'r-', 
            label = f'$R^2$ = {r2}')

    ax.legend(loc = "lower right")

def load_and_concat(lat, site, year):
    
    epbs = pd.read_csv("EPBs_DRIFT.txt", 
                       index_col = 0)
    epbs.index = pd.to_datetime(epbs.index)
    
    epbs = epbs.loc[epbs["lat"] == lat]
    
    drf = load_drift(site = site, 
                     ext = str(year))
    
    drf = drf.loc[:, ["vx", "vy"]]
    
    df = pd.concat([epbs, drf], 
                   axis = 1).dropna()
    
    df = df.loc[df["vy"] > 0]
    
    return df


site = "FZA"
year = 2015
lat = -5


df = load_and_concat(lat, site, year) 


times = [
         dt.time(0, 0), dt.time(1, 0), 
         dt.time(2, 0), dt.time(3, 0), 
         dt.time(4, 0), dt.time(5, 0)
         ]



fig, ax = plt.subplots(figsize = (12, 8), 
                       sharey = True, 
                       sharex = True,
                       ncols = 3, 
                       nrows = 2)

for n, ax in enumerate(ax.flat):
    df1 = df.loc[df.index.time == times[n]]

    x, y = df1["V_1"].values, df1["vx"].values
    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)


    regression_model = LinearRegression()
    # Fit the data(train the model)
    regression_model.fit(x, y)
    # Predict
    y_predicted = regression_model.predict(x)

    ax.scatter(x, y)
    ax.plot(x, y_predicted, "r")
    ax.set(title = times[n])

fontsize = 20
fig.text(0.05, 0.45, "DRIFT", rotation = "vertical", 
         fontsize = fontsize)

fig.text(0.5, 0.05, "EPBs", rotation = "horizontal", 
         fontsize = fontsize )

fig.suptitle(f"DRIFT ({site}) e Deriva de EPBs ({lat}°) - {year}")
