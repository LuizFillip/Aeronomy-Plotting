import PlasmaBubbles as pb 
import events as ev 
import matplotlib.pyplot as plt 


def plot_epbs_by_solar_cycle(
        path = 'events.txt',
        col_flux = 'f107a',
        period = 'sunset'
        ):
    

    fig, ax = plt.subplots(
        nrows = 3, 
        dpi = 300, 
        figsize = (12, 10), 
        sharex = True, 
        sharey = True
        )
    
    ds = load_data(
        path,
        period = period, 
        col_flux = col_flux
        )
        
    events = ev.solar_flux_cycles(
            ds, 
            flux_col = col_flux,
            lower_level = 74, 
            high_level = 107
            )
    
    epb_col = ds.columns[:-1]
    
    all_total = ds[epb_col].values.sum()
    
    count = 0
    for i, even in enumerate(events):
        
        total = int(even[epb_col].values.sum())
        
        count += total
        days  = len(even)
        
        info = f'EPBs = {total}\n Days = {days}'
        
        ax[i].text(
            0.4, 0.5, 
            info, 
            transform = ax[i].transAxes
            )
        
        ds1 = percentual_occurrence(even)
        
            
        for col in epb_col:
        
            ds1[col] = (ds1[col] / all_total) * 100
    
                
        ds1.plot(
            ax = ax[i], 
            kind = 'bar', 
            legend = False
            )
    
    print(all_total, count)
    ax[0].legend(
        ncols = 5, 
        bbox_to_anchor = (.5, 1.6), 
        loc = "upper center", 
        title = 'longitudinal sectors'
        )
    
    return #events


# percentual_occurrence(ds)

plot_epbs_by_solar_cycle(
    col_flux = 'f107', 
        period = 'midnight'
        )
