import events as ev

args = dict(
    capsize = 3,
    marker = 's'
    )
 
def plot_distribution(
        ax, 
        df, 
        label = '', 
        count = True
        ):
    
    step = 0.2
    
    
    ds = ev.probability_distribuition(
        df,
        step = step
        )
    
    # ds.drop(
    #     ds.tail(2).index, 
    #     inplace = True
    #     )
    
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
        
    return 



