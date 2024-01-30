import pandas as pd
import matplotlib.pyplot as plt
import base as b 
import RayleighTaylor as rt

b.config_labels(fontsize = 25)

def pipe_data():
    
    df = b.load('20131224tlt.txt')
    
    df['vp'] = 25
    
    ds = rt.add_gammas(df)
    
    ds['gr'] = ds['ge'] / ds['nui']
    
    ds['K'] = ds['K'] *1e5
    ds['gamma'] = ds['gamma'] *1e3
    
    return ds

def plot_growth_rate_parameters():
    fig, ax = plt.subplots(
        nrows = 5,
        figsize = (12, 14),
        sharex = True,
        dpi = 300
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    
    ds = pipe_data()
    
    cols = ['ratio', 'K', 
            'mer_perp',
            'gr', 'gamma']
    
    lims = [[0.5, 1.1], 
            [-1, 6], 
            [-6, 0], 
            [0, 10], 
            [0, 2]]
    for i, col in enumerate(cols):
        
        ax[i].plot(ds[col])
        
        ax[i].set(
            ylabel = b.y_label(col),
            ylim = lims[i])
        
        
    b.format_time_axes(ax[-1], translate = True)
    
    b.plot_letters(ax, y = 0.7, x = 0.03)

    return fig

     

fig = plot_growth_rate_parameters()


FigureName = 'gamma_parameters'

fig.savefig(
    b.LATEX(FigureName, 
            folder = 'timeseries'),
    dpi = 400
    )