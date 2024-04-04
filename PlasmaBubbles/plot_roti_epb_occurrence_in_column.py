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


def plot_occurregram(ax):
    
    return 

def plot_roti_epb_occurrence_in_column(
        df, 
        ds, 
        fontsize = 30):
    
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
        
        terminator = pb.terminator(
            int(col), 
            dn, 
            float_fmt = False
            )
        
        ds.loc[ds.index < terminator] = 0
    
        ax[i, 0].plot(df[col])
        ax[i, 1].plot(ds[col])
        
        ax[i, 0].axhline(0.25, lw = 2, color = 'r')
         
        l = b.chars()[i]
       
        for col in [0, 1]:
            ax[i, col].text(
                0.01, 0.8, f'({l}) Setor {i + 1}°', 
                transform = ax[i, col].transAxes
                )
            ax[i, col].axvline(
                terminator, color = 'k', lw = 2)
            
            b.format_time_axes(ax[-1, col])
            
        ax[i, 0].set(ylim = [0, vmax + 1])
        
        ax[i, 1].set(ylim = [-0.1, 1.1])
        
    b.format_time_axes(ax[-1, 0])
    
    
          
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

df = b.load('events_class3')

ds = df.loc[(df['lon'] ==-50) & 
            (df['type'] == 'midnight') & 
            (df['drift'] == 'fresh')]

ds = ds.loc[ds.index > dt.datetime(2017,1,30)]
b.make_dir('temp/')

def save(ds):
    for dn in ds.index:
    
        # dn = dt.datetime(2018, 1, 13, 21)
        # 
        print('', dn)
        plt.ioff()
        
        delta = dt.timedelta(hours = 21)
        ds, df = load_dataset(dn + delta, hours = 14)
        try:
            fig = plot_roti_epb_occurrence_in_column(df, ds)
        except:
            continue
        name = dn.strftime('temp/%Y%m%d')    
        fig.savefig(name)
        
        plt.clf()
        plt.close()


# ds
dn = dt.datetime(2016, 5, 29, 21)
ds, df = load_dataset(dn, hours = 14)
fig = plot_roti_epb_occurrence_in_column(df, ds)