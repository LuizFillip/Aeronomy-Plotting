import events as ev
import base as b 

def plot_distribution(
        ax, 
        df, 
        name, 
        step = 0.2, 
        col_gamma = 'all',
        col_epbs = '-40'
        ):
    
    

    ds = ev.probability_distribuition(
        df,
        step = step, 
        col_gamma = col_gamma,
        col_epbs = col_epbs
        )

    args = dict(
        capsize = 3,
        marker = 's'
        )
    
    ax.errorbar(
        ds['mean'], 
        ds['rate'], 
        xerr = ds['std'],
        yerr = ds['epb_std'],
        **args,
        label = name
        )
    

    for bar in [0, 1]:
        ax.axhline(
            bar, 
            linestyle = ":", 
            lw = 2, 
            color = "k"
            )
        
    return ds['epbs'].sum()




import matplotlib.pyplot as plt 



fig, ax = plt.subplots(
    ncols = 2,
    nrows = 2, 
    figsize = (14, 8), 
    sharex = True, 
    sharey = True, 
    dpi = 300
    )

ks = {
     
     3: 'march equinox',
     6: 'june solstice',
     9: 'setember equinox',
     12: 'december solstice'
    
     }

plt.subplots_adjust(wspace = 0.1)

df = b.load('all_results.txt')

df['doy'] = df.index.day_of_year

def kp_levels(df):
    quiet = df[df['kp_max'] <= 3]
    
    disturbed = df[df['kp_max'] > 3]
    
    return [quiet, disturbed]

for i, ax in enumerate(ax.flat):
    
    month = (i + 1) * 3
    season_name = ks[month]
    
    out = []
    name = ['$Kp \\leq 3$', '$Kp > 3$']
    
    for i, level in enumerate(kp_levels(df)):
        
        ds = ev.seasons(level, month)
    
        c = plot_distribution(
                ax, 
                ds, 
                name[i]
                )
        
        out.append(c)
    
    ax.set(title = season_name.title())


ax.legend(ncol = 2)