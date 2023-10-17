
import PlasmaBubbles as pb 
import matplotlib.pyplot as plt
import base as b 


def plot_seasonal_occurrence(ds):
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 1,
        sharex = True,
        figsize = (12, 4)
        )

    period = ['sunset']
    
    plt.subplots_adjust(hspace = 0.1)
        
    df =  pb.month_occurrence(
        ds, 1
        )
    
    
    df.plot(
        kind = 'bar', 
        ax = ax, 
        legend = False
        )

    
    plt.xticks(rotation = 0)
    
    ax.set(
        ylabel = 'Nigths with EPB',
        xlabel = 'Months',
        xticklabels = b.number_to_months()
        )
        
    t = df.sum().values
    c = ds.columns
    ax.legend(
        [f'{c[i]}° ({t[i]})' for i in range(len(c))],
        ncol = 5, 
        title = f'Longitudinal sectors (2013 - 2022)',
        bbox_to_anchor = (.5, 1.4), 
        loc = "upper center", 
        columnspacing = 0.6
        )
    
    
    

path = 'database/epbs/events_types.txt'

ds = b.load(path)

ds

# from geophysical_indices import INDEX_PATH
# import pandas as pd
 

# df = pd.concat(
#     [b.load(path), 
#      b.load(INDEX_PATH)], 
#     axis = 1).dropna()


# ds = df.loc[df['kp'] > 3].iloc[:, :5]


plot_seasonal_occurrence(ds)


