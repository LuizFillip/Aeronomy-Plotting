import digisonde as dg
import base as b 

def plot_dhF(cols):
    
    for c in cols:
        x = ds[c].dropna()
        y = b.filter_frequencies(x.values)
        ax[2, col].plot(x.index, c * 10 + y)
        ax[2, col].set(ylim = [0, 100])