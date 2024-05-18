import matplotlib.pyplot as plt 
import base as b 
import PlasmaBubbles as pb 
import datetime as dt
import numpy as np 
import GEO as gg 

b.config_labels(fontsize = 25)

def load_dataset(dn, hours = 12, root = 'D:\\'):
    
    
    out = []
    for folder in ['events', 'longs']:
        
        infile = f'database/epbs/{folder}/{dn.year}'
        ds = b.load(infile)
        
        out.append(b.sel_times(ds, dn, hours = hours))
        
    return tuple(out)


def get_infos(ds, lon):
    df1 = pb.BubbleFeatures(ds)
    
    infos = df1.loc[df1.index.get_level_values(1) == lon, 
                   ['type', 'drift']].values.ravel()
    
    Type = infos[0]
    Drift = infos[1]
    
    if Type == Drift:
        return f'{Type}'
    else:
        return f'{Type} - {Drift}'


def plot_roti_epb_occurrence_in_column(
        dn, 
        fontsize = 30, 
        threshold = 0.25
        ):
    
    fig, ax = plt.subplots(
        nrows = 4,
        ncols = 1, 
        dpi = 300, 
        sharey = 'col',
        sharex = True,
        figsize = (10, 12)
        )

    plt.subplots_adjust(hspace = 0.3, wspace = 0.2)
    
    ds, df = load_dataset(dn, hours = 12)
    
    vmax = np.ceil(df.values.max())
    
    lons = df.columns
        
    for i, ax in enumerate(ax.flat):
        
        lon = lons[i]
        
        terminator = gg.terminator(
            int(lon), 
            dn, 
            float_fmt = False
            )
        
        ds.loc[ds.index < terminator] = 0
    
        ax.plot(df[lon])
        
        ax1 = ax.twinx()
        
        # print(ds.columns)
        try:
            ax1.plot(ds[lon])
        except:
            ax1.plot(ds[int(lon)])
            
        
        ax.axhline(threshold, lw = 2, color = 'r')
         
        l = b.chars()[i]
       
        ax.text(
            0.01, 1.05, f'({l}) Setor {i + 1}°', 
            transform = ax.transAxes
            )
        ax.axvline(terminator, color = 'k', lw = 2)
                    
        ax.set(
            ylim = [0, vmax + 1], 
            xlim = [df.index[0], df.index[-1]],
            # title = get_infos(ds, lon = int(lon)) 
            )
        
        ax1.set(ylim = [-0.1, 1.1])
        
        if i == 3:
            b.format_time_axes(ax)
    
    fig.text(
        0.04, 0.33, 
        'ROTI (TECU/min)', 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.95, 0.45, 
        'Ocorrência', 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    return fig 


dn = dt.datetime(2013, 5, 15, 21)

fig = plot_roti_epb_occurrence_in_column(dn)

plt.show()

