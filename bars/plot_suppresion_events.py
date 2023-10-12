from geophysical_indices import INDEX_PATH
import pandas as pd
import base as b
import PlasmaBubbles as pb 
import numpy as np


path = 'database/epbs/events_types.txt'


# df = pd.concat(
#     [b.load(path), 
#      b.load(INDEX_PATH)], 
#     axis = 1).dropna()


# ds = df.loc[df['kp'] > 3].iloc[:, :5]

ds = b.load(path)


        
        
def remove_middle(arr):
    middle_index = len(arr) // 2

    if len(arr) % 2 == 0:
        
        arr = np.delete(arr, [middle_index - 1, middle_index])
    else:
       
        arr = np.delete(arr, middle_index)

    return arr

    


ds

import PlasmaBubbles as pb 
import matplotlib.pyplot as plt
import base as b 


def plot_sunset_midnight_events(ds):
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        sharex = True,
        figsize = (12, 4)
        )

    # period = ['sunset', 'midnight']
    
    plt.subplots_adjust(hspace = 0.1)
    # ylims = [350, 40]
    # for i, value in enumerate([1, 3]):
        
    df =  pb.month_occurrence(
        ds, 0
        )
    
    total = int(df.values.sum())

    
    df.plot(
        kind = 'bar', 
        ax = ax, 
        legend = False
        )
    
    # title = f'({b.chars()[i]}) Post {period[i]} '
    # events = f'({total}  events)'
    
    plt.xticks(rotation = 0)
    
    # ax.text(
    #     0.03, 0.85, 
    #     title + events, 
    #     transform = ax.transAxes
    #     )
    
    ax.set(
        ylabel = 'Nigths without EPB',
        xticklabels = b.number_to_months(), 
        # ylim = [0, ylims[i]]
        )
        
    period_type = '$Kp > 3$'
    ax.legend(
        [f'{c}°' for c in ds.columns],
        ncol = 5, 
        title = f'Longitudinal sectors (2013 - 2022)',
        bbox_to_anchor = (.5, 1.4), 
        loc = "upper center", 
        columnspacing = 0.6
        )
    
    ax.set(xlabel = 'Months')
    
    
#

def find_supressions(ds):
    
    ds['value'] = pb.event_for_all_longs(
        ds, 
        value = 1
        )
    
    out = []
    
    for i, row in enumerate(ds['value']):
    
        if row == 0:
    
            lst = ds.iloc[i - 2: i + 3, -1]
            
            lst_remo = remove_middle(lst.values)
            
            if all(x == 1 for x in lst_remo):
               
                out.append(ds.iloc[i, :-1].to_frame().T)
            else:
                pass
    
    return pd.concat(out)

df = find_supressions(ds)

df_filtered = df[df.apply(
    lambda row: 
    all(x == 0 for x in row), axis=1)
        ]
    
plot_sunset_midnight_events(df_filtered)

'''

teve EPB: 2013-01-26 

'''
df_filtered