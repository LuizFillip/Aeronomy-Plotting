import matplotlib.pyplot as plt
import PlasmaBubbles as pb 
import datetime as dt
import base as b 
import GNSS as gs

args = dict(
    marker = 'o', 
    markersize = 1,
    linestyle = 'none', 
    alpha = 0.5,
    color = 'k'
    )


def plot_receivers_amount_vad(df, receivers):
    
    num = len(receivers)
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (10, 10),
        sharex = True,
        sharey = True,
        nrows = num
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    for i, receiver in enumerate(receivers):
        
        l = b.chars()[i]
        
        ds = df.loc[df['sts'].isin(receiver)]
       
        ax[i].plot(
            ds['roti'], **args, 
            label = f'{len(ds)} ROTI points'
            )
        
        info = f'({l}) {len(receiver)} receivers'
        
        ax[i].text(
            0.01, 0.75, info,
            transform = ax[i].transAxes
            )
     
        ax[i].legend(loc = 'upper right')
        ax[i].set(ylim = [0, 3])
    
    b.format_time_axes(ax[num - 1], hour_locator = 3)