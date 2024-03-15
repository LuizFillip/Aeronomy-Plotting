import pandas as pd
import core as c
import matplotlib.pyplot as plt 


def plot_time_shift_of_epbs(df):

    fig, ax = plt.subplots(
        figsize = (14, 12),
        dpi = 300,
        nrows = 4,
        sharex = True,
        sharey = True
        )
    
    
    for hour, ax in enumerate(ax.flat):
        
        ds = df.loc[
            (df['shift'] >= hour) & 
            (df['shift'] < hour + 1)].replace(
             ('no_epb', 'sunset', 'midnight'), (0, 1, 1))
        
        
        
        df1 = pd.pivot_table(
              ds, 
              columns = 'lon', 
              values = 'type', 
              index = ds.index
              ).replace(float('NaN'), 0)
        
        
        ds = c.count_occurences(df1)
        
        ds.month.plot(kind = 'bar', ax = ax, legend = False)
        
        info = f'{hour} $< \delta t <$ {hour + 1}'
        ax.text(0.4, 0.75, info, transform = ax.transAxes)
        
        if hour == 0:
            ax.legend(loc = 'upper center', ncol = 4, 
                      bbox_to_anchor = (.5, 1.4),
                      )
