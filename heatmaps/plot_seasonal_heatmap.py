import PlasmaBubbles as pb 
import base as b 
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 

def plot_heatmap(ax, df,  year = 2018):
    
    ds1 = df.loc[df.index.year == year]
    ds1 = pb.concat_months(ds1, col)
    
    sns.heatmap(
        ds1, 
        ax = ax, 
        cbar_kws = {
            'pad': .02, 
            'label': "Ocorrência",
            'ticks': np.arange(0, 1.25, 0.25),
            },
        linecolor='white',
        vmax = 1,
        vmin = 0
        )
    
    ax.set(ylabel = 'Meses', 
            xlabel = 'Hora universal', 
            title = year)

    
path = 'all_events'
df = b.load(path)
col = '-50'
year = 2013


def plot_seasonal_heatmap(df):
    
    fig, ax = plt.subplots(
        ncols = 2, 
        dpi = 300, 
        sharex = True, 
        sharey = True,
        figsize = (16, 6)
        )

    plot_heatmap(ax[0], df,  year = 2013)
    
    plot_heatmap(ax[1], df,  year = 2018)