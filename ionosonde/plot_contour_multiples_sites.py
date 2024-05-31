import matplotlib.pyplot as plt
import digisonde as dg
import base as b 
import GEO as gg 
import plotting as pl

 
CHAR_PATH = 'digisonde/data/chars/midnight/'

def plot_site(ax, col, file):
    

    ds, vz, site = pl.pipe_data(file)
     
    dn = ds.index[0]
    
    cols = ds.columns[3:-5]
    
    cols = list(range(2, 7, 1))
    
    pl.plot_heights(ax[0, col], ds, cols)
    
    pl.plot_drift(ax[1, col], vz, cols, site)
    
    for c in cols:
        x = ds[c].dropna()
        y = b.filter_frequencies(x.values)
        ax[2, col].plot(x.index, c * 10 + y)
        ax[2, col].set(ylim = [0, 100])
        
    ax[0, col].set(title = gg.sites[site]['name'])
    
    b.format_time_axes(ax[-1, col], hour_locator = 2)
    
    d = gg.dusk_from_site(
            dn, 
            site = site,
            twilight_angle = 18
            )
    
    ax[0, col].axvline(d, lw = 2)
    ax[1, col].axvline(d, lw = 2)
    ax[2, col].axvline(d, lw = 2)
    for a in ax.flat:
        a.set(ylabel = '')
       
        
       
    ax[-1, 0].set(ylabel = 'd(hF) (km)')
    ax[0, 0].set(ylabel = 'Altitude (km)')
    ax[1, 0].set(ylabel = 'Vertical drift (m/s)')

 
def plot_two_ionossonde_parameters():
    
    fig, ax = plt.subplots(
        figsize = (18, 14), 
        nrows = 3, 
        ncols = 3,
        sharex = True, 
        sharey = 'row', 
        dpi = 300
        )

    plt.subplots_adjust(hspace = 0.05, wspace= 0.05)

    plot_site(ax, 0, 'FZA0M_20220724(205).TXT')
           
    plot_site(ax, 1, 'SAA0K_20220724(205).TXT')

    plot_site(ax, 2, 'CAJ2M_20220724(205).TXT')
  
    ax[0, 0].legend(
        ncol = 6, 
        loc = "upper right", 
        title = 'Frequencies (MHz)',
        bbox_to_anchor = (2.4, 1.6), 
        )
    
    b.plot_letters(ax, y = 0.85, x = 0.03)
    
    return fig



fig = plot_two_ionossonde_parameters()
FigureName = 'frequencies_vz_saa_fza'
# fig.savefig(
#       b.LATEX(FigureName, folder = 'paper2'),
#       dpi = 400
#       )