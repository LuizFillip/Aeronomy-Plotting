import matplotlib.pyplot as plt
import base as b
import PlasmaBubbles as pb
import core as c
import pandas as pd 

def join_data(year = 2019, lon = -70):
    
    df = c.potential_energy(year)
    
    df = df.loc[(
        (df['Lon'] >= lon - 10) &
        (df['Lon'] <= lon) 
        )]
    
    df = df.resample('1M').mean()
    
    df.index = df.index.month
    
    ds = c.clima_epb(year = year, sec = 'month')
    
    df = pd.concat([ds[lon], df['mean_90_110']], axis = 1)
    
    df = df.rename(
        columns = {lon: 'epb',
                   'mean_90_110': 'ep'}
        )
    
    return  df


def plot_month(
        ax, 
        x, y
        ,
        norm = True
        ):
    

    ax.scatter(x, y, s = 30)
    
    fit = b.linear_fit(x, y)
    
    intercept = round(fit.intercept, 2)
    slope = round(fit.slope[0], 2)
    r2 = str(fit.r2_score)
    
    ax.plot(x, fit.y_pred, 
            lw = 2, color = 'r')
    
    info = '$R^2 = $' + f'{r2}'
    ax.text(
        0.2, 0.8, 
        info, 
        transform = ax.transAxes
        )
    
    return ax


def plot_correlation_epb_Ep(
        flux = 'f107a',
        roti = 'mean', 
        lon = -40,
        norm = True
        ):
    
    sectors = [-50, -60, -70]
        
    fig, ax = plt.subplots(
        dpi = 300, 
        sharex = True, 
        sharey = True,  
        ncols = len(sectors), 
        figsize = (14, 6)
        )
    
    plt.subplots_adjust(wspace = 0.1)
    
    for i, sector in enumerate(sectors):
        
        ds = join_data(lon = sector)
        
        x = ds['ep'].values
        y = ds['epb'].values
        

        plot_month(
            ax[i], 
            x, y, 
            norm = norm
            )
        
        ax[i].set(title = f'Sector: {sector}')
        


    return fig

fig = plot_correlation_epb_Ep()





