import events as ev

args = dict(
    capsize = 3,
    marker = 's'
    )
 
def plot_distribution(
        ax, 
        df, 
        limits,
        col = 'gamma',
        label = '', 
        count = True,
        drop = 2
        ):

    ds = ev.probability_distribuition(
        df,
        limits,
        col = col
        )
        
    if drop is not None:
        ds.drop(
            ds.tail(drop).index, 
            inplace = True
            )
    
    epbs = ds['epbs'].sum()
    
    if count:
        LABEL = f'{label} ({epbs} events)'
    else:
        LABEL = label
    
    ax.errorbar(
        ds['mean'], 
        ds['rate'], 
        xerr = ds['std'],
        yerr = ds['epb_error'],
        label = LABEL,
        **args
        )
    

    for bar in [0, 1]:
        ax.axhline(
            bar, 
            linestyle = ":", 
            lw = 2, 
            color = "k"
            )
        
    return epbs 



