import PlasmaBubbles as pb 
import base as b 
import numpy as np
import matplotlib.pyplot as plt 
import core as c 
import pandas as pd 


def plot_seasonal_hourly(
        df2, 
        df,
        cmap = 'jet',
        fontsize = 35, 
        translate = False,
        sector = 1
        ):
    
    if translate:
        ylabel = 'Months'
        xlabel = 'Universal time'
        
        zlabel = 'Occurrence (\%)'
        title = f'Seazonal/hourly occurrence on sector {sector}'
    else:
        ylabel = 'Meses'
        xlabel = 'Hora universal'
        zlabel = 'Ocorrência (\%)'
        title = f'Ocorrência sazonal/horária no setor {sector}'
   

    fig, ax = plt.subplots(
          dpi = 300, 
          sharex = True, 
          sharey = True,
          figsize = (12, 6)
          )
        
    
    yticks = df2.index 
    xticks = df2.columns 
    img = ax.imshow(
          df2.values,
          aspect = 'auto', 
          extent = [xticks[0], xticks[-1], 
                    yticks[-1], yticks[0]],
          cmap = cmap
          )
    
    percent = True
    
    if percent:
        factor = 100
        units = ' (\%)'
    else:
        factor = 1
        units = ''
         
    ticks =  np.arange(0, 1.25 * factor, 0.25 * factor)
    
    b.colorbar(
        img, 
        ax,
        ticks = ticks, 
        label = f"Occurrence{units}", 
        anchor = (.08, 0., 1, 1)
        )
    
    ax.plot(df.index, df['dusk'], lw = 2, color = 'w')
    ax.axhline(27, lw = 2, color = 'w')
    
    
    ax.text(0.01, 0.3, 'Local midnight', 
            color = 'w',
            transform = ax.transAxes)
    
    ax.text(0.01, 0.9, 'Sunset (300 km)', 
            color = 'w',
            transform = ax.transAxes)
    
    yticks = np.arange(yticks[0], yticks[-1], 2)
    yticklabels = np.where(yticks >= 24, yticks - 24, yticks)
    
    ax.set(
           yticks = yticks,
           yticklabels = yticklabels,
           xlim = [xticks[0], xticks[-1]],
           
           xlabel = 'Years',
           ylabel = 'Universal time'
       )
    return fig


def annual_hourly_occurrence(ds, step = 0.5):
    

    df = ds.loc[(ds['lon'] == -50) & 
                (ds.index.year < 2023)] 
    
    start = df.index[0].year
    end = df.index[-1].year 
    
    out = []
    for year in range(start, end + 1):
        
        out.append(pb.hourly_distribution(
            df.loc[df.index.year == year], 
            step = step, 
            percent  = False))
        
        
    dat = np.concatenate(out).T
    
    dat /= dat.max() 
    dat *= 100
    
    dates = pd.date_range(
        f'{start}-01-01', 
        f'{end}-12-31', 
        freq = '1M')
    
    
    times = np.arange(20, 32, step)
     
    return df, pd.DataFrame(dat, index = times, columns = dates)


ds = b.load('events_class2')


df, df2 = annual_hourly_occurrence(ds, step = 0.5)

fig = plot_seasonal_hourly(
        df2, 
        df,
        cmap = 'jet',
        fontsize = 35, 
        translate = False,
        sector = 1
        )