import matplotlib.pyplot as plt 
import base as b
import core as c

b.config_labels(fontsize = 28)

args = dict(
    edgecolor = 'black', 
    color = 'gray', 
    linewidth = 1.5
    )

def plot_annually_epbs_and_indices(
        df,
        solar_level = 86,
        kp_level = 3
        ):
    
    fig, ax = plt.subplots(
        nrows = 3, 
        dpi = 300, 
        figsize = (14, 12)
        )
    
    plt.subplots_adjust(hspace = 0.1)
        
    ds = c.year_occurrence(df)
    
    ds['epb'].plot(kind = 'bar', ax = ax[2], 
        legend = False,
        **args
        )
     
    ax[0].plot(df['f107'])
        
    ax[0].plot(df['f107a'], lw = 2)
    
    ax[1].bar(df.index, df['kp'], 
              width = 1,
              alpha= 0.5, 
              color = 'gray')
    
    mean = df['kp'].resample('1M').mean()
    
    ax[1].plot(
        mean, label = 'Monthly average',
        lw = 3, color = 'k')
    
    ax[1].legend()
    
    ax[0].set(
        xlim = [df.index[0], df.index[-1]],
        ylabel = '$F_{10.7}$ (sfu)', 
        ylim = [50, 300],
        yticks = list(range(50, 350, 50))
        )
    
    ax[1].set(
        xlim = [df.index[0], df.index[-1]],
        ylabel = 'Kp index', 
        yticks = list(range(0, 10, 3))
        )
    
    ax[2].set(
        ylabel = 'Nights with EPB',
        xlabel = 'Years', 
        yticks = list(range(0, 350, 100))
        )
    
    ax[0].axhline(solar_level, color = 'r', lw = 2)
    
    ax[1].axhline(kp_level, color = 'r', lw = 2)
    
    fig.autofmt_xdate(rotation = 0, ha = 'center')

    for i, ax in enumerate(ax.flat):
       
       l = b.chars()[i]
       ax.text(
           0.02, 0.83, f'({l})', 
           transform = ax.transAxes
           )
    
    return fig

df = c.concat_results('saa')
df = c.epbs(geo = True)
fig = plot_annually_epbs_and_indices(df)

fig.savefig(b.LATEX('annual_variation'))