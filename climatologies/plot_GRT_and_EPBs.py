import matplotlib.pyplot as plt
import base as b 
import core as c




b.config_labels()

def plot_percent_contribuitions():

    fig, ax = plt.subplots(
        sharex = True,
        dpi = 300, 
        figsize = (14, 8), 
        )
    
    plt.subplots_adjust(hspace = 0.1)

    df = c.gamma('saa', el_upper = False)

    df = df.resample('1M').mean()
    
    cols = ['drift', 'gravity', 'winds', 'gamma']
    
    for col in cols:
        
        ax.plot((df[col] / df['gamma']) * 100, label = col)
        
    ax.legend(
        ncol = 4, 
        loc = 'upper center', 
        bbox_to_anchor = (0.5, 1.2)
        )
    
    ax.set(ylabel = 'Percentual de contribuição (\%)')

# plot_percent_contribuitions()

# df = c.gamma('saa', el_upper = False )

