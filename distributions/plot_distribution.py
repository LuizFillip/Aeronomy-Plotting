import events as ev

def plot_distribution(
        ax, 
        df, 
        label = '', 
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
        yerr = ds['epb_error'],
        **args,
        label = label
        )
    

    for bar in [0, 1]:
        ax.axhline(
            bar, 
            linestyle = ":", 
            lw = 2, 
            color = "k"
            )
        
    return ds['epbs'].sum()



