import matplotlib.pyplot as plt 
import datetime as dt 
import events as ev 

def sel_year(ds, yr):
    ds1 = ds.loc[ds.index.year == yr]
    
    ds1['occ'] = yr 
    
    return ds1




def plot_scatter_occorrence(
        ax, ds, month = 3
        ):
    
    names_seasons = {
         
         3: 'march equinox',
         9: 'setember equinox',
         12: 'december solstice',
         6: 'june solstice'
         
         }
    
    dn = dt.date(2013, month, 21)
    
    ys = ds.index[0] 
    ye = ds.index[-1] 
    
    years = list(range(ys.year, ye.year))
    for yr in years:
        
        ds1 = sel_year(ds, yr)
        
        ax.scatter(ds1.doy, ds1.occ, color = 'k', s = 20)
        
        ax.scatter(ev.get_doy(dn), yr, s = 80, color = 'r')
        
    name = names_seasons[month]
    
    
    ax.set(yticks = years,  
            title = f'{name} ({dn.strftime("%d/%m")})')


def plot_seasons_disponibility(df):
    
    fig, ax = plt.subplots(
        ncols = 2,
        nrows = 2,
        sharey = True, 
        figsize = (14, 8)
        )
    
    
    plt.subplots_adjust(
        hspace = 0.35, wspace = 0.1)
    
    for i, ax in enumerate(ax.flat):
        
        month = (i + 1) * 3
        
     
        ds = ev.season(df, month)
        
        plot_scatter_occorrence(
            ax, ds, month = month)

