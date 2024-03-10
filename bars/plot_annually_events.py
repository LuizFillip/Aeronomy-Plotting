import core as c
import matplotlib.pyplot as plt
import base as b 

b.config_labels(fontsize = 25)


def plot_annualy_variation(ds, years):
    
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(
        nrows = 2,
        ncols = len(years) // 2,
        dpi = 300, 
        sharex = True,
        sharey = True,
        figsize = (14, 8)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    for i, ax in enumerate(ax.flat):
        year = years[i]
        # ds1 = locate_sector_year(ds, year, long = -80)
        ds.plot(kind = 'bar', ax = ax)
        
        ax.text(0.5, 0.8, year, transform = ax.transAxes)
        
        ax.set(ylabel = 'Noites com EPBs')
        
    return fig
    
    

def plot_annually_events_count(ds):
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        sharex = True,
        figsize = (14, 6)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    df = c.CountAllOccurences(ds).year
        
    df.plot(
        kind = 'bar', 
        ax = ax, 
        legend = False
        )
    
    plt.xticks(rotation = 0)
    
    ax.set(
        ylabel = 'Noites com EPB',
        xlabel = 'Anos'
        )
        
    t = [f'{col}° ({vl})' for col, vl in zip(ds.columns, df.sum().values)]
    
    ax.legend(
        t,
        ncol = 5, 
        title = 'Setores longitudinais e eventos de EPBs (2013 - 2022)',
        bbox_to_anchor = (.5, 1.3), 
        loc = "upper center", 
        columnspacing = 0.6
        )
    return fig

typing = 'sunset'
# typing = 'postmidnight'
path = f'database/epbs/{typing}_events3.txt'
ds = b.load(path)

fig = plot_annually_events_count(ds)

# FigureName = 'annualy_midnight_sunset'

# fig.savefig(
#     b.LATEX(FigureName, folder = 'bars'),
#     dpi = 400
#     )
