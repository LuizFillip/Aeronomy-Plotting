import matplotlib.pyplot as plt
import digisonde as dg
import base as b 
import GEO as gg 
import plotting as pl

 
CHAR_PATH = 'digisonde/data/chars/midnight/'

def plot_site(ax, col, file):
    
    
    ds, vz, site = pl.pipe_data(file)
    
    cols = ds.columns[3:-5]
    
    cols = list(range(3, 7, 1))
    pl.plot_heights(ax[col, 0], ds, cols)
    
    pl.plot_drift(ax[col, 1], vz, cols, site)
    
    ax[col, 0].set(title = gg.sites[site]['name'])
    ax[col, 1].set(title = gg.sites[site]['name'])
    
    
    if col == 2:
        b.format_time_axes(ax[2, 0], translate = False)
        b.format_time_axes(ax[2, 1], translate = False)
    

 
def plot_two_ionossonde_parameters():
    
   

    fig, ax = plt.subplots(
        figsize = (16, 14), 
        nrows = 3, 
        ncols = 2,
        # sharey = 'col',
        sharex = True, 
        dpi = 300
        )

    plt.subplots_adjust(hspace = 0.3, wspace= 0.3)


    file = 'FZA0M_20220724(205).TXT'

    plot_site(ax, 0, file)
           
    file = 'SAA0K_20220724(205).TXT'

    plot_site(ax, 1, file)

    file = 'CAJ2M_20220724(205).TXT'

    plot_site(ax, 2, file)
  
    ax[0, 0].legend(
        ncol = 2, 
        loc = "upper right", 
        title = 'Frequencies (MHz)'
        )
    
    b.plot_letters(ax, y = 0.85, x = 0.03)
    
    return fig



fig = plot_two_ionossonde_parameters()
FigureName = 'frequencies_vz_saa_fza'
# fig.savefig(
#       b.LATEX(FigureName, folder = 'paper2'),
#       dpi = 400
#       )