import cartopy.crs as ccrs
import GEO as gg
import base as b 
import matplotlib.pyplot as plt
import PlasmaBubbles as pb
import datetime as dt
import plotting as pl 


b.config_labels(fontsize = 30)

def load_data(dn, root = 'D:\\'):
    
    df = pb.concat_files(dn, root)
    
    return b.sel_times(df, dn, hours = 0.5)
    

def plot_regions_ipp_and_sites(dn):
    
    fig, ax = plt.subplots(
        dpi = 300,
        ncols = 2, 
        sharex = True, 
        figsize = (14, 14),
        subplot_kw = {'projection': ccrs.PlateCarree()}
    )
    
    plt.subplots_adjust(wspace = 0.2)
    
    sites = ['car',  'jic', 'saa'] 
    names = [  
             'Imager (Cariri)', 
             'Digisonde (Jicamarca)', 
             'Digisonde (São Luis)'
             ]  
    
    df = load_data(dn)
    
    for i in range(2):
        
       gg.map_attrs(ax[i], dn.year)
       
       corners = pl.plot_corners(
               ax[i],
               dn.year,
               radius = 10,
               label = False 
               )
    
       gg.plot_sites_markers(ax[i], sites, names)
       
       l = b.chars()[i]
       
       ax[i].text(
           0.05, 0.9, f'({l})', fontsize = 30,
                  transform = ax[i].transAxes)
       
    pl.plot_ipp_on_map(ax[1], df, corners)
       
    gg.stations_near_of_equator(
        ax[0],
         dn.year,
         distance = 5, 
         extra_sts = [])
        
    ax[1].set(ylabel = '', 
           yticklabels = [])
    
    
    ax[0].legend(loc = 'upper center',
                 ncol = 3, 
                 bbox_to_anchor = (1.05, 1.2), 
                 columnspacing = 0.2)
    
    plt.show()
    
    return fig

def main():
    
    dn = dt.datetime(2013, 1, 14, 23)
    
    fig = plot_regions_ipp_and_sites(dn)
    
    FigureName = 'regions_and_ipp'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'maps'),
        dpi = 400
        )
    
# main()