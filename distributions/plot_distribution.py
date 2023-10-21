import events as ev

def plot_distribution(
        ax, 
        df, 
        label = '', 
        step = 0.2
        ):

    ds = ev.probability_distribuition(
        df,
        step = step
        )
    
    # ds.drop(
    #     ds.tail(2).index, 
    #     inplace = True
    #     )
    
    args = dict(
        capsize = 3,
        marker = 's'
        )
    
    ax.errorbar(
        ds['mean'], 
        ds['rate'], 
        xerr = ds['std'],
        yerr = ds['epb_error'],
        label = label,
        **args
        )
    

    for bar in [0, 1]:
        ax.axhline(
            bar, 
            linestyle = ":", 
            lw = 2, 
            color = "k"
            )
        
    return ds['epbs'].sum()



