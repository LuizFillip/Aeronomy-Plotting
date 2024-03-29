import matplotlib.pyplot as plt 
import base as b 
import PlasmaBubbles as pb 
import datetime as dt
import numpy as np 


b.config_labels(fontsize = 25)

def load_dataset(dn, hours = 12, num = 3, root = 'D:\\'):
    
    out = []
    for folder in [f'events{num}', f'long{num}']:
        ds = b.load(
            pb.epb_path(
                f'{dn.year}', 
                root = root, 
                folder = folder
                )
            )
        
        out.append(b.sel_times(ds, dn, hours = hours))
        
    return tuple(out)


def plot_roti_epb_occurrence_in_column(
        df, ds, fontsize = 30):
    
    fig, ax = plt.subplots(
        nrows = 4,
        ncols = 2, 
        dpi = 300, 
        sharey= 'col',
        sharex= True,
        figsize = (18, 10)
        )

    plt.subplots_adjust(hspace = 0.1, wspace = 0.2)

    dn = df.index[0]
    vmax = np.ceil(df.values.max())
    
    for i, col in enumerate(df.columns):
        
        terminator = pb.terminator(int(col), dn, float_fmt = False)
        
        ds.loc[ds.index < terminator] = 0
    
        ax[i, 0].plot(df[col])
        ax[i, 1].plot(ds[col])
        
        ax[i, 0].axhline(0.25, lw = 2, color = 'r')
        
        terminator = pb.terminator(int(col), dn, float_fmt = False)
        
        ax[i, 1].axvline(terminator, color = 'k', lw = 2)
        ax[i, 0].axvline(terminator, color = 'k', lw = 2)
        
        l = b.chars()[i]
        ax[i, 0].text(
            0.01, 0.8, f'({l}) {col}°', 
            transform = ax[i, 0].transAxes
            )
        
        ax[i, 1].text(
            0.01, 0.8, f'({l}) {col}°', 
            transform = ax[i, 0].transAxes
            )
    
        ax[i, 0].set(ylim = [0, vmax])
        
    b.format_time_axes(ax[-1, 0])
    b.format_time_axes(ax[-1, 1])
    
          
    fig.text(
        0.07, 0.33, 
        'ROTI (TECU/min)', 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.5, 0.39, 
        'Ocorrência', 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    return fig 



dn = dt.datetime(2015, 10, 29, 20) 

ds, df = load_dataset(dn, hours = 12)

fig = plot_roti_epb_occurrence_in_column(df, ds)