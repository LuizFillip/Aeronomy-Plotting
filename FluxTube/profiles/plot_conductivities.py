import matplotlib.pyplot as plt
import base as b 
import numpy as np
import plotting as pl 


b.config_labels(fontsize = 25)


lbs = b.Labels()




def plot_height_prf(ax, df, col):
   
    
    ds = df.loc[df['hem'] == 'north']
    ax.plot(b.smooth2(ds[col], 10), ds.index, 
            label = 'Norte', color = 'b', lw = 1)
    
    ds1 = df.loc[df['hem'] == 'south']
    ax.plot(b.smooth2(ds1[col], 10), ds1.index, 
            label = 'Sul', color = 'r', lw = 1)
    
    total = ds[col] + ds1[col]
    
    ax.plot(b.smooth2(total, 10), total.index, 
            label = 'Total', lw = 1, color = 'k')
    
    
    ax.set(xlabel = f'$\Sigma_P^{col}$'
        )
    

    return total


def plot_conductivities(df):
    
    fig, ax = plt.subplots(
        ncols = 3, 
        sharey= True,
        dpi = 300, figsize = (12, 6))
    
    
    plt.subplots_adjust(wspace = 0.1, hspace = 0.1)
    
    out = []
    for i, col in enumerate(['E', 'F']):
        
        total = plot_height_prf(ax[i], df, col)
        
        out.append(total)
        
    ratio = out[1] / (out[1] + out[0]) 
    
    ax[2].plot(b.smooth2(ratio, 2), ratio.index, 
               lw = 1, label = 'Total', color = 'k')

    ax[2].set(xlabel = '$\\frac{\Sigma_P^F}{\Sigma_P^F + \Sigma_P^E}$',
              xlim = [0.6, 1.0],
              xticks = np.arange(0.5, 1.1, 0.2),
              )
    
    ax[0].set(ylabel = 'Altura de Apex (km)', 
              xticks = np.arange(0, 8, 1))
    
    ax[1].set(xticks = np.arange(10, 100, 20))
    
    ax[0].legend(ncol = 3,
                 bbox_to_anchor = (1.5, 1.2),
                 loc = "upper center")
    
    return fig
    
ds = pl.load_fluxtube()
fig = plot_conductivities(ds)


# FigureName = 'conductivities'

# fig.savefig(
#     b.LATEX(FigureName, folder = 'profiles'),
#     dpi = 400
#     )
