import matplotlib.pyplot as plt
import base as b 
import events as ev 

def plot_gamma(ax, df):
    
    # df = df * 1e3
    
    ax.scatter(
        df.index, df, 
        s = 30,
        alpha = 0.4, 
        color = 'gray'
        )
    
    avg = b.smooth2(df, 20)
    ax.plot(
        df.index, 
        avg, 
        lw = 2
        )
    
    ax.set(
        ylim = [-0.2, 3], 
        ylabel = b.y_label('gamma'),
        xlim = [df.index[0], df.index[-1]]
        )
    
    ax.axhline(avg.max(), linestyle = '--')
    ax.axhline(avg.min(), linestyle = '--')
    
    return df


b.config_labels()

lbs = b.Labels().infos


fig, ax = plt.subplots(
    sharex = True,
    dpi = 400, 
    nrows = 3, 
    figsize = (14, 8), 
    )

plt.subplots_adjust(hspace = 0.1)

df = ev.concat_results('saa', class_epb = 'sunset')


plot_gamma(ax[1], df['gamma'])

df = ev.epbs(geo = True)
ax[0].plot(df['f107'])
ax[0].plot(df['f107a'], lw = 2)
ax[0].set(ylabel = 'F10.7 (sfu)')
ax[0].axhline(86, lw = 2, color = 'r')
ds = ev.month_to_month_occurrence(
        df, 
        col = 'epb'
        )

args = dict(
    facecolor = 'lightgrey', 
    edgecolor = 'black', 
    # width = 0.5,
    width = 20,
    color = 'gray', 
    linewidth = 1
    )


ax[2].bar(ds.index, ds['epb'].ravel(), **args)
ax[2].set(ylabel = 'Nights with EPBs',
           ylim = [0, 40],
           xlabel = 'Years'
          )

for i, ax in enumerate(ax.flat):
    
    l = b.chars()[i]
    ax.text(
        0.02, 0.85, f'({l})', 
        transform = ax.transAxes
        )

plt.show()

