import PlasmaBubbles as pb 
import base as b 
import matplotlib.pyplot as plt 
import plotting as pl  
b.config_labels()





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



def plot_seasonal_hourly_all_sectors(
        df, 
        fontsize = 35, 
        translate = False,
        sector = 1
        ):
    
    fig, ax = plt.subplots(
           ncols = 1,
           nrows = 4,
           dpi = 300, 
           sharex = True, 
           sharey = True,
           figsize = (16, 14)
           )

    plt.subplots_adjust(wspace = 0.05)
     
    sectors = {-50: 1, -60: 2, -70: 3, -80: 4}


    for sector, row in sectors.items():
        
        df = ds.loc[(ds['lon'] == sector) ] 
      
        df2 = pb.hourly_annual_distribution(df, step = 1)
        
        pl.plot_terminator(ax[row - 1], sector)
        
        pl.plot_seasonal_hourly(
            ax[row - 1],
            df2, 
            cmap = 'jet',
            fontsize = 35, 
            translate = True,
            heatmap = True, 
            colorbar = False, 
            levels = 10
            )
        
        ax[row - 1].set(ylabel = '', title = f'Setor {row}')
        
        

    if translate:
        ylabel = 'Universal time'
        xlabel = 'Years'
        zlabel = 'Occurrence (\%)'
    else:
        xlabel = 'Anos'
        ylabel = 'Hora universal'
        zlabel = 'Ocorrência (\%)'


    b.fig_colorbar(
            fig,
            vmin = 0, 
            vmax = 100, 
            cmap = "jet",
            fontsize = 25,
            step = 10,
            label = zlabel, 
            sets = [0.32, 0.98, 0.4, 0.02], 
            orientation = 'horizontal', 
            levels = 30
            )
        
    fig.text(
        0.5, 0.05,
        xlabel, 
        fontsize = fontsize
        )

    fig.text(
        0.045, 0.41, 
        ylabel, 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
     
    return fig
    

def main():

    ds = b.load('events_class2')
    
    
    ds = ds.loc[(ds['type'] == 'midnight') & 
                (ds['drift'] == 'fresh')]
    
    fig = plot_seasonal_hourly_all_sectors(
            ds, 
            fontsize = 35, 
            translate = False,
            sector = 1
            )
    
    FigureName = 'seasonal_hourly_all_sectors'
    
    fig.savefig(
          b.LATEX(FigureName, 'climatology'),
          dpi = 400)
    
