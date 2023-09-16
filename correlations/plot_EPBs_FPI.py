import matplotlib.pyplot as plt
import base as b
import pandas as pd 
def plot_corr_EPB_FPI(fontsize = 20):
    
    df = b.load('roti_evo.txt')

    ip = b.load('database/indices/indeces.txt')


    ip

    df = df.loc[df['lon'] == -40]

    # df['mean'].plot()

    # df['base'].plot()

    # ip = b.load('database/indices/solar_flux.txt')

    # import numpy as np

    # # ip = ip.replace((-1, 0), np.nan)
    ds = pd.concat([df, ip], axis = 1).dropna()

    ds = ds.loc[ds.index.day == 5]
      
    print(ds)


    fig, ax = plt.subplots(
        dpi = 300, 
        sharex = True, 
        figsize = (10, 4)
        )

    x, y = ds['f107'].values / 100, ds['mean'].values

    ax.scatter(x, y)

    r2, ypred = b.linear_fit(x, y)

    ax.plot(x, ypred, lw = 2, color = 'r', label = r2)

    ax.set(xlim = [0, 3], ylim = [0, 3])
    ax.legend()

    


plot_corr_EPB_FPI(fontsize = 20)