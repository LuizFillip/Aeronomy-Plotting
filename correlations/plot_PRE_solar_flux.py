import matplotlib.pyplot as plt
import base as b 
import os 
import core as c 
import datetime as dt 
import GEO as gg
import pyIGRF 


site = 'jic'

def set_data(site):
    years = '2013_2021.txt'
        
    PATH_PRE = 'digisonde/data/PRE/'
    
    path = os.path.join(
        PATH_PRE,
        site, 
        years
        )    
    df = b.load(path)
    df = df.rename(columns = {'vz':'vp'})
    df = df.loc[~(df['vp'] >100)]
    
    df['doy'] = df.index.day_of_year 
    df['dec'] = df.index.to_series().apply(
        lambda dn: mag_dec(dn=dn, site=site))

    df['e'] = df['doy'].apply(b.declination)
    df['alpha'] = df['dec'] - df['e']

    ds = c.geo_index()
    
    df['f107a'] =  df.index.map(ds['f107a'])
    return df.dropna()


def mag_dec(dn, site = 'jic'):
   
    lat, lon = gg.sites[site]["coords"]
    
    D, I, H, X, Y, Z, F = pyIGRF.igrf_value(
                lat, 
                lon, 
                alt = 300, 
                year = gg.year_fraction(dn)
                )
    
    return D

b.config_labels(fontsize = 30)

def plot_alpha(ax, site, col = 'alpha'):
    df = set_data(site)
    
    x = df[col].values
    y =  df['vp'].values
    
    ax.scatter(x, y, s = 5)
    
    fit = b.linear_fit(x, y)
     
    ax.plot(x, fit.y_pred, lw = 3, color = 'red')

    ax.text(
        0.4, 0.85, 
        f'$R^2$ = {fit.r2_score}', 
        transform = ax.transAxes) 

    if col == 'alpha':
        xlabel = '$\\alpha$ (°)'
    else:
        xlabel = '$F_{10,7}$ (sfu)'
    
    ax.set(
        xlabel = xlabel ,
        # title = name, 
           ylim = [0, 100])

    return None 

 
fig, ax = plt.subplots(
    ncols = 2, 
    nrows = 2,
    dpi = 300, 
    sharey = True, 
    figsize =(12, 12), 
    # sharex = 'col'
    )

plt.subplots_adjust(
    hspace = 0.25, 
    wspace = 0.05
    )

plot_alpha(ax[0, 0], site = 'saa', col = 'f107a')
plot_alpha(ax[1, 0], site = 'saa')

ax[0, 0].set(title = gg.sites['saa']['name'], 
             ylabel = '$V_P$ (m/s)')
plot_alpha(ax[0, 1], site = 'jic')
plot_alpha(ax[1, 1], site = 'jic', col = 'f107a')


ax[0, 1].set(title = gg.sites['jic']['name'])
ax[1, 0].set(ylabel = '$V_P$ (m/s)')

b.plot_letters(
       ax, 
       y = 0.85, 
       x = 0.02, fontsize = 40)
