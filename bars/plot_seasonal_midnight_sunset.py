import PlasmaBubbles as pb 
import matplotlib.pyplot as plt
import base as b 


def plot_sunset_midnight_events(ds):
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        sharex = True,
        figsize = (12, 8)
        )

    period = ['sunset', 'midnight']
    
    plt.subplots_adjust(hspace = 0.1)
    ylims = [350, 40]
    for i, value in enumerate([2, 4]):
        
        df =  pb.month_occurrence(
            ds, value
            )
        
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
        
    period_type = '$Kp > 3$'
    ax[0].legend(
        [f'{c}°' for c in ds.columns],
        ncol = 5, 
        title = f'Longitudinal sectors (2013 - 2022) {period_type}',
        bbox_to_anchor = (.5, 1.4), 
        loc = "upper center", 
        columnspacing = 0.6
        )
    
    ax[1].set(xlabel = 'Months')
    
    

# path = 'database/epbs/events_types.txt'

# ds = b.load(path)

# from geophysical_indices import INDEX_PATH
# import pandas as pd
 

# df = pd.concat(
#     [b.load(path), 
#      b.load(INDEX_PATH)], 
#     axis = 1).dropna()


# ds = df.loc[df['kp'] > 3].iloc[:, :5]


# plot_sunset_midnight_events(ds)


