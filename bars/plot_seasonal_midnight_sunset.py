import PlasmaBubbles as pb 
import matplotlib.pyplot as plt
import base as b 
import events as ev 

b.config_labels()

def plot_sunset_midnight_events(ds):
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        sharex = True,
        figsize = (12, 8)
        )

    period = ['sunset', 'midnight']
    
    plt.subplots_adjust(hspace = 0.1)
    ylims = [350, 40]
    for i, value in enumerate([2, 4]):
        
      
        
        df =  pb.month_occurrence(
            ds, value
            )
        
        total = int(df.values.sum())
    
        
        df.plot(
            kind = 'bar', 
            ax = ax[i], 
            legend = False
            )
        
        title = f'({b.chars()[i]}) Post {period[i]} '
        events = f'({total}  events)'
        
        plt.xticks(rotation = 0)
        
        ax[i].text(
            0.03, 0.85, 
            title + events, 
            transform = ax[i].transAxes
            )
        
        ax[i].set(
            ylabel = 'Nigths with EPB',
            xticklabels = b.number_to_months(), 
            ylim = [0, ylims[i]]
            )
        
    period_type = '$Kp > 3$'
    ax[0].legend(
        [f'{c}°' for c in ds.columns],
        ncol = 5, 
        title = f'Longitudinal sectors (2013 - 2022) {period_type}',
        bbox_to_anchor = (.5, 1.4), 
        loc = "upper center", 
        columnspacing = 0.6
        )
    
    ax[1].set(xlabel = 'Months')
    

def plot_seasonal(ax, ds):

    df = ev.monthly_occurrences(ds)
        
    df['epb'].plot(
        kind = 'bar', 
        ax = ax, 
        legend = False
        )
        
    ax.set(
        ylabel = 'Nigths with EPB',
        xlabel = 'Months',
        ylim = [0, 100]
        )
    
    ax.set_xticklabels(b.number_to_months(), rotation=0)
    
    
    
def plot_annually(ax, ds):

    df = ev.yearly_occurrences(ds)
        
    df['epb'].plot(
        kind = 'bar', 
        ax = ax, 
        legend = False
        )
        
    ax.set(
        ylabel = 'Nigths with EPB',
        xlabel = 'Years',
        ylim = [0, 100]
        )
    
    plt.xticks(rotation = 0)





def plot_annual_seasonal(ds):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        figsize = (12, 8)
        )
    
    plt.subplots_adjust(hspace = 0.3)
    
    
    plot_seasonal(ax[0], ds)
    plot_annually(ax[1], ds)
    
   

ds = ev.epbs(
        col = -70, 
        class_epb = 'midnight',
        geo = False
        )

plot_annual_seasonal(ds)