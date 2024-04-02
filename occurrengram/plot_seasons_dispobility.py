import matplotlib.pyplot as plt 
import datetime as dt 
import core as c 
import base as b

names_seasons = {
     
     3: 'march equinox',
     9: 'setember equinox',
     12: 'december solstice',
     6: 'june solstice'
     
     }

def sel_year(ds, yr):
    ds1 = ds.loc[ds.index.year == yr]
    
    ds1['occ'] = yr 
    
    return ds1


def plot_scatter_occorrence(
        ax, ds, month = 3
        ):
    
    
    
    dn = dt.date(2013, month, 21)
    
    ys = ds.index[0] 
    ye = ds.index[-1] 
    
    
    years = list(range(ys.year, ye.year + 1))
    for yr in years:
        
        ds1 = sel_year(ds, yr)
        
        ax.scatter(ds1.doy, ds1.occ, color = 'k', s = 10)
        
        ax.scatter(c.dn2doy(dn), yr, s = 60, color = 'r')
        
    name = names_seasons[month]
    
    
    ax.set(
        ylim = [ys.year - 1, ye.year + 2],
        yticks = years
        )
    
    return name
    


def plot_seasons_disponibility(
        df, 
        fontsize = 30
        ):
    
    fig, ax = plt.subplots(
        ncols = 2,
        nrows = 2,
        sharey = True, 
        figsize = (16, 10)
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.05
        )
    
    for i, ax in enumerate(ax.flat):
        
        month = (i + 1) * 3
        
        ds = c.seasons(df, names_seasons[month])
        
        name = plot_scatter_occorrence(
            ax, 
            ds, 
            month = month
            )
        
        l = b.chars()[i]
        ax.text(
            0.03, 0.9, f'({l}) {name}', 
            transform = ax.transAxes
            )
    
    fig.text(
        0.03, 0.45, 
        'Years',
        rotation = "vertical", 
        fontsize = fontsize
        )

    fig.text(
        0.5, 0.07, 
        "Doy", 
        rotation = "horizontal", 
        fontsize = fontsize
        )
    
    return fig

# df = c.concat_results('saa')

# df['doy'] = df.index.day_of_year.copy()
# fig = plot_seasons_disponibility(df)

