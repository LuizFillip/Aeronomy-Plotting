import base as b 
import matplotlib.pyplot as plt

df = b.load('events_class2')


def plot_EPBs_durations(df, fontsize = 30):
    fig, ax = plt.subplots(
        nrows = 4,
        sharex = True, 
        sharey = True,
        figsize = (12, 10),
        dpi = 300
        )
    
    
    plt.subplots_adjust(hspace = 0.1)
    
    lons = df['lon'].unique()[::-1]
    
    for i, lon in enumerate(lons):
        
        ds = df.loc[df['lon'] == lon, 'duration']
        ax[i].plot(ds)
        
        l = b.chars()[i]
        
        ax[i].text(
            0.02, 0.75, 
            f'({l}) Setor {i + 1}', 
            transform = ax[i].transAxes)
        
        ax[i].set(ylim = [0, 15])
    
    ax[-1].set_xlabel('Anos', fontsize = fontsize)
    
    fig.text(
        0.05, .32, 
        'Duração somado (horas)', 
        rotation = 'vertical', 
        fontsize = fontsize
        )