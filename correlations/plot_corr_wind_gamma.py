import matplotlib.pyplot as plt
import pandas as pd
from base import load, Labels, linear_fit

def plot_corr_wind_gamma(ds, df):
    
    
    x = ds['mer_parl'].values
    y = ds['all_perp'].values
    
    
    fig, ax = plt.subplots(
        dpi = 300
        )
    ax.scatter(x, y)
  
    lbs = Labels()
    r2, fit = linear_fit(x, y)
    
    ax.plot(x, fit, 
            color = "r", 
            lw = 2, 
            label = f"$R^2$ = {r2}")
    
    ax.set(xlabel = '$U_L^P \\parallel$ to B', 
           ylabel = lbs.label)
    
    ax.legend()
    
# file = 'database/Results/all_parameters/saa_2013_2015.txt'

# df = load(file)

# import seaborn as sns 
# cols = ['parl_mer', 'F10.7adj', 'all']
# df = df[cols].groupby(df.index).first()
# sns.pairplot(df)

