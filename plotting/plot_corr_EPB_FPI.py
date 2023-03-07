import matplotlib.pyplot as plt
from FabryPerot.core import load_FPI
from liken.utils import get_fit
from liken.core import load_EPB

def plot_corr_EPB_FPI(fontsize = 20):
    
    FPI = load_FPI()

    EPB = load_EPB('EPBs_DRIFT.txt', lat = -5)

    df = EPB.join(FPI).dropna()
    
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
        
        r2, y_predicted = get_fit(x, y)
        
        ax.set(title = f"Mês: {n}")
        ax.scatter(x, y)
        ax.plot(x, y_predicted, "r", 
                label = f"$R^2$ = {r2}")
        
        ax.legend(loc = "lower right")
        
    
    fig.text(0.04, 0.45, "EPBs",
             rotation = "vertical", 
             fontsize = fontsize)
    
    fig.text(0.5, 0.06, "FPI", 
             rotation = "horizontal", 
             fontsize = fontsize)
    
plot_corr_EPB_FPI(fontsize = 20)

