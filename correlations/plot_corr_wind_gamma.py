import matplotlib.pyplot as plt
from utils import linear_fit
import pandas as pd

def plot_corr_wind_gamma(ds, df):
    
    ds = pd.concat([ds['mer_parl'], 
                    df['all_perp']], 
                   axis = 1).dropna()
    
    ds = ds.loc[~(ds['all_perp'] > 20)]
    
    x = ds['mer_parl'].values
    y = ds['all_perp'].values
    
    
    fig, ax = plt.subplots()
    ax.scatter(x, y)
  
    
    r2, fit = linear_fit(x, y)
    
    ax.plot(x, fit, 
            color = "r", 
            lw = 2, 
            label = f"$R^2$ = {r2}")
    
    ax.set(xlabel = '$U_L^P \\parallel$ to B', 
           ylabel = lbs.label)
    
    ax.legend()