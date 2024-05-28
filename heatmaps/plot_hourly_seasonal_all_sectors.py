import PlasmaBubbles as pb 
import base as b 
import matplotlib.pyplot as plt 
import core as c 
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
    



ds = b.load('events_class2')
# plot_f107(ax[0])




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
    
    df = ds.loc[(ds['lon'] == sector) & (ds.index.year < 2023)] 
    
    df2 = pb.hourly_annual_distribution(df, step = 1)
    
    pl.plot_seasonal_hourly(
        ax[row - 1],
        df2, 
        cmap = 'jet',
        fontsize = 35, 
        translate = True,
        heatmap = True, 
        colorbar = False
        )
    
    pl.plot_terminator(ax[row - 1], df, sector)
    
    
FigureName = 'seasonal_hourly_{sector}'

    
# fig.savefig(
#     b.LATEX(FigureName, 'climatology'),
#     dpi = 400)