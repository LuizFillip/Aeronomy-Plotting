import matplotlib.pyplot as plt 
import digisonde as dg 
import datetime as dt 
import base as b 


def plot_profiles_density_grads(df, year, month):
    fig, ax = plt.subplots(
            ncols =2,
            figsize = (10, 8),
            dpi = 300,
            sharey = True
            )
    plt.subplots_adjust(wspace = 0.1)
    
    for i in range(5, 10):
        dn = dt.datetime(year, month, i, 1, 0)
        
        ds = df.loc[(df.index == dn)]
        ax[0].plot(ds['ne'], ds['alt'], label = i)
        ax[1].plot(ds['L']*1e5, ds['alt'], label = i)
        ax[0].set(xlabel = 'Electron density (m3)', 
                  xlim = [0, 1.5e12])
        ax[1].set(xlabel = 'L (m2)', xlim = [-6, 6])
        ax[0].axhline(300)
        ax[1].axhline(300)
        
    plt.legend(title = 'days')
    ax[0].set(ylabel = 'Altura (km)')
    fig.suptitle(dn.strftime('%B-%Y (%Hh%M)'))
    
    return fig

year = 2015



infile = f'digisonde/data/jic/profiles/{year}'

df = dg.load_profilogram(infile)
# df['L'] = b.smooth(df['L'], 20)
time = dt.time(1, 0)

for month in [1, 6]:
    plot_profiles_density_grads(df, year, month)