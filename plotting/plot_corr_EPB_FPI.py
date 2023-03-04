import pandas as pd
import matplotlib.pyplot as plt
from FabryPerot.core import load_FPI
from Liken.utils import get_fit2

def load_EPB(lat = -5):
    df = pd.read_csv("EPBs_DRIFT.txt", index_col = 0)
    df.index = pd.to_datetime(df.index)
    return df.loc[df["lat"] == lat, ["vel"]]



def plot_corr_EPB_FPI():
    
    df = pd.concat([load_EPB(lat = -5), 
                    load_FPI().loc[:, ["zon"]]], 
                   axis = 1).dropna()
    
    fig, ax = plt.subplots(figsize = (12, 8), 
                           sharey = True, 
                           sharex = True,
                           ncols = 3, 
                           nrows = 2)
    
    plt.subplots_adjust(wspace = 0.05)
    
    months = [1, 2, 3, 10, 11, 12]
    
    for n, ax in zip(months, ax.flat):
        df1 = df.loc[df.index.month == n]
        
        y = df1["vel"].values
        x = df1["zon"].values
        
        x = x.reshape(-1, 1)
        y = y.reshape(-1, 1)
        
        r2, y_predicted = get_fit2(x, y)
        
        ax.set(title = f"Mês: {n}")
        ax.scatter(x, y)
        ax.plot(x, y_predicted, "r", 
                label = f"$R^2$ = {r2}")
        
        ax.legend(loc = "lower right")
        
        
        
    fontsize = 20
    
    fig.text(0.04, 0.35, "EPBs",
             rotation = "vertical", 
             fontsize = fontsize)
    
    fig.text(0.4, 0.08, "FPI", 
             rotation = "horizontal", 
             fontsize = fontsize)