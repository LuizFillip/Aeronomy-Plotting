import numpy as np 
import matplotlib.pyplot as plt
import base as b 
import core as c

b.config_labels()

def plot_sunset_midnight_events(ds):
    
    
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
        
        df = c.month_occurrence(ds)
        df = df.loc[df['type'] == value].iloc[:, :-1]
        df = df.replace(np.nan, 0)
        total = int(df.values.sum())
        df.plot(
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
            xticklabels = b.number_to_months(), 
            ylim = [0, ylims[i]]
            )
        
    # period_type = '$Kp > 3$'
    ax[0].legend(
        [f'{c}°' for c in ds.columns],
        ncol = 5, 
        title = f'Longitudinal sectors (2013 - 2022)',
        bbox_to_anchor = (.5, 1.4), 
        loc = "upper center", 
        columnspacing = 0.6
        )
    
    ax[1].set(xlabel = 'Months')
    
    return fig

ds = c.epbs(class_epb = None)

# ds

fig = plot_sunset_midnight_events(ds)

FigureName = 'seasonal_midnight_sunset'

fig.savefig(
    b.LATEX(FigureName, folder = 'bars'),
    dpi = 400
    )
