import matplotlib.pyplot as plt
import base as b 
import events as ev 
    
args = dict(
    edgecolor = 'black', 
    color = 'gray', 
    linewidth = 1
    )

def plot_seasonal(ax, ds):

    df = ev.monthly_occurrences(ds)
        
    df['epb'].plot(
        kind = 'bar', 
        ax = ax, 
        legend = False, **args
        )
        
    ax.set(
        ylabel = 'Nigths with EPB',
        xlabel = 'Months',
        ylim = [0, 80]
        )
    
    ax.set_xticklabels(b.number_to_months(), rotation=0)
    
    
    
def plot_annually(ax, ds):

    df = ev.yearly_occurrences(ds)
        
    df['epb'].plot(
        kind = 'bar', 
        ax = ax, 
        legend = False, **args
        )
        
    ax.set(
        ylabel = 'Nigths with EPB',
        xlabel = 'Years',
        )
    
    plt.xticks(rotation = 0)





def plot_annual_seasonal(ds):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        sharey = True,
        ncols = 2,
        figsize = (16, 4)
        )
    
    plt.subplots_adjust(wspace = 0.05)
    
    
    plot_seasonal(ax[0], ds)
    plot_annually(ax[1], ds)
    
    for i, ax in enumerate(ax.flat):
       
       l = b.chars()[i]
       ax.text(
           0.02, 0.83, f'({l})', 
           fontsize = 35,
           transform = ax.transAxes
           )
    
    return fig 

ds = ev.epbs(
        col = -50, 
        class_epb = 'midnight',
        geo = False
        )

fig = plot_annual_seasonal(ds)

save_in = 'G:\\Meu Drive\\Doutorado\Travels\\seasonal_yearly'

fig.savefig(save_in, dpi = 300)