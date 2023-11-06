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
    nrows = 2, 
    figsize = (24, 8), 
    )

plt.subplots_adjust(hspace = 0.1)

df = ev.concat_results('saa', class_epb = 'sunset')


plot_gamma(ax[0], df['gamma'])

df = ev.epbs(geo = True)

# df = df.loc[df['kp'] > 3]

ds = ev.month_to_month_occurrence(
        df, 
        col = 'epb'
        )



# ds = ev.yearly_occurrences(df)


args = dict(
    facecolor = 'lightgrey', 
    edgecolor = 'black', 
    # width = 0.5,
    width = 15,
    color = 'gray', 
    linewidth = 1
    )


ax[1].bar(ds.index, ds['epb'].ravel(), **args)
ax[1].set(ylabel = 'Nights with EPBs',
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

