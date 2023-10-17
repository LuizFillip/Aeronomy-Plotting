import PlasmaBubbles as pb 
import events as ev 
import matplotlib.pyplot as plt 
import base as b

path = 'database/epbs/events_types.txt'


def plot_epbs_by_solar_cycle(
        path = 'events.txt',
        col_flux = 'f107a',
        period = 'sunset'
        ):
    

    fig, ax = plt.subplots(
        nrows = 2, 
        dpi = 300, 
        figsize = (12, 10), 
        sharex = True, 
        sharey = True
        )
    
    ds = b.base(path)
   

    
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
