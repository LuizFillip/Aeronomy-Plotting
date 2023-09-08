import datetime as dt
import base as b 
import matplotlib.pyplot as plt
import PlasmaBubbles as pb 




def plot_epbs_occurrences_roti(
        ds, 
        window = 10, 
        threshold = 0.5
        ):

    fig, ax = plt.subplots(
        nrows = 2, 
        dpi = 300, 
        sharex = True, 
        figsize = (10, 6)
        )
    
    b.config_labels()
    
    plt.subplots_adjust(hspace = 0.1)
    
    ax[0].plot(ds)
    
    ax[0].set(
        ylim = [0, 6], 
        yticks = list(range(6)),
        ylabel = 'ROTI (TECU/min)'
        )

    
    ax[0].legend(
        ds.columns, 
        ncol = 5, 
        title = 'Longitudinal zones',
        bbox_to_anchor = (.5, 1.5), 
        loc = "upper center"
        )
    
    ax[0].axhline(
        threshold, 
        lw = 2, 
        color = 'k', 
        linestyle = '--'
        )
    
    infos = f' (a) Threshold = {threshold} TECU/min'
    
    ax[0].text(0.05, 0.8, infos, 
               transform = ax[0].transAxes)
        
    
    ax[1].plot(
        pb.get_events(
            ds, window = window, 
            threshold = threshold
            )
        )
    
    ax[1].set(ylabel = 'EPBs occurence', 
              yticks = [0, 1], 
              ylim = [-0.2, 1.2])
    
    infos = f'(b) $\\Delta t$ = {window} min'
    
    ax[1].text(0.05, 0.8, 
               infos, 
               transform = ax[1].transAxes)
    
    b.format_time_axes(ax[1])
    
    return fig
    
year = 2013
# infile = f'database/EPBs/longs/{year}.txt'
infile = f"D:\\database\\epbs\\longs\\{year}.txt"

dn = dt.datetime(year, 3, 17, 21)

df = b.load(infile)

ds = b.sel_times(df, dn, hours = 9)
    
fig = plot_epbs_occurrences_roti(ds)
# ds.plot()
