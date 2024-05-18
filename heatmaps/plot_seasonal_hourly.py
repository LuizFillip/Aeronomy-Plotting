import PlasmaBubbles as pb 
import base as b 
import numpy as np
import matplotlib.pyplot as plt 
import core as c 

b.config_labels()


def plot_heatmap(
        ax, 
        values, 
        percent = True, 
        colorbar = True,
        step = 1
        ):
  
    yticks = np.arange(1, 13, 1)
    xticks = np.arange(20, 32 + step, step*2)
    
    if percent:
        factor = 100
        units = ' (\%)'
    else:
        factor = 1
        units = ''
        
    ticks =  np.arange(0, 1.25 * factor, 0.25 * factor)
 
    
    img = ax.imshow(
        values,
        aspect = 'auto', 
        extent = [20, 32, 12, 0],
        cmap = 'magma'
        )
        
    xticklabels = np.where(xticks >= 24, xticks - 24, xticks)
    yticklabels = b.month_names(sort = True, language = 'pt')
   
    if colorbar:
        b.colorbar(
            img, 
            ax,
            ticks = ticks, 
            label = f"Ocorrência{units}"
            )
   
   
    ax.set(
        xticks = xticks, 
        yticks = yticks - 0.5,
        xticklabels = xticklabels, 
        yticklabels = yticklabels
        )
    
    return 


def divide_by_geomgnetic_levels(df):
    
    cond = [
        df['kp'] <= 3, 
        (df['kp'] > 3) & 
        (df['kp'] <= 6), 
        df['kp'] > 6]
    
    labels = [
    '$Kp \\leq 3$', '$ 3 < Kp \\leq  6$', "$Kp > 6$"
    ]    
    
    
    return cond, labels



def plot_seasonal_hourly(
        df, 
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
          ncols = 4,
          nrows = 3,
          dpi = 300, 
          sharex = True, 
          sharey = True,
          figsize = (16, 14)
          )

    plt.subplots_adjust(wspace = 0.15)
    
    years = list(range(2013, 2024, 1))

    for i, ax in enumerate(ax.flat):
        
        
        try:
            year = years[i]
            sel_year = df.loc[df.index.year == year]
            
            ds = pb.hourly_distribution(sel_year, step = 0.5)
    
            plot_heatmap(ax, ds, colorbar = False)
            
            df1 = df.loc[df.index.year == 2020]
            
            ax.plot(df1['dusk'], df1['day'], lw = 3, color = 'w')
            
            ax.set(title = year)
        
        except:
            ax.axis('off')
        
   
    fig.text(
        0.45, 0.05,
        xlabel, 
        fontsize = fontsize
        )
    
    fig.text(
        0.03, 0.45, 
        ylabel, 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    
    #sets = [0.3, 0.99, 0.4, 0.02] upper part
    
    b.fig_colorbar(
            fig,
            vmin = 0, 
            vmax = 100, 
            cmap = 'magma',
            fontsize = 25,
            step = 20,
            label = zlabel, 
            sets = [0.77, 0.12, 0.03, 0.23] 
            )
    
    fig.suptitle(title)
    return fig
    




sectors = {-50: 1, -60: 2, -70: 3, -80: 4}

def main():
    col = -50
    
    
    typing = 'midnight'
    
    for col, sector in sectors.items():
    
        df = c.sel_epb_typing(col, typing)
        
        fig = plot_seasonal_hourly(df, sector = sector)
        
        
        FigureName = f'seasonal_hourly_{sector}'
        
            
        fig.savefig(
            b.LATEX(FigureName, 'climatology'),
            dpi = 400)
        plt.show()
    
main()