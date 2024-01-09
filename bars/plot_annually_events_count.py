import core as c
import matplotlib.pyplot as plt
import base as b 
import numpy as np

b.config_labels()

def plot_annually_events_count(ds):
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        sharex = True,
        figsize = (12, 8)
        )

    period = ['sunset', 'midnight']
    
    plt.subplots_adjust(hspace = 0.1)
    
    ylims = [350, 100]
    
    for i, value in enumerate(period):
        
        df =  c.year_occurrence( ds )
        
        df1 = df.loc[df['type'] == value].iloc[:, :-1]
        # df = df.replace(np.nan, 0)
        print(df1)
        
        total = int(df1.values.sum())
    
        df1.plot(
            kind = 'bar', 
            ax = ax[i], 
            legend = False
            )
        
        title = f'({b.chars()[i]}) Post {period[i]} '
        events = f'({total}  events)'
        
        plt.xticks(rotation = 0)
        
        ax[i].text(
            0.03, 0.85, 
            title + events, 
            transform = ax[i].transAxes
            )
        
        ax[i].set(
            ylabel = 'Nigths with EPB',
            ylim = [0, ylims[i]]
            )
        
   
    ax[0].legend(
        [f'{c}°' for c in ds.columns],
        ncol = 5, 
        title = 'Longitudinal sectors (2013 - 2022)',
        bbox_to_anchor = (.5, 1.4), 
        loc = "upper center", 
        columnspacing = 0.6
        )
    
    ax[1].set(xlabel = 'Years')
    
    return fig
ds = c.epbs(class_epb = None)

fig = plot_annually_events_count(ds)

FigureName = 'annualy_midnight_sunset'

fig.savefig(
    b.LATEX(FigureName, folder = 'bars'),
    dpi = 400
    )
