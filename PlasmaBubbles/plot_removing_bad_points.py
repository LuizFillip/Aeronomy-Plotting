import PlasmaBubbles as pb
import matplotlib.pyplot as plt 
import base as b 
import datetime as dt 
import matplotlib.dates as dates 


    




 
args = dict(marker = 'o', 
             markersize = 1,
             linestyle = 'none', 
             color = 'k'
             )


def plot_section(ax, df, dn, i = 1):
    
    

    df = b.sel_times(df, dn, hours = 0.6)
    
    ax.plot(df['roti'], **args)
    
    std = df['roti'].std()
    avg = df['roti'].mean()
     
    ax.axhline(avg, lw = 2, color = 'g')
    

    ax.fill_between(df.index, 
                    avg + i * std, 
                    avg - i * std, 
                    alpha = 0.2, 
                    color = 'darkgreen'
                    )
    
    
    b.format_minutes_axes(ax)
    
    ax.set(ylim = [-0.2, 5], 
            xlabel = 'Universal time', 
            ylabel = 'ROTI'
            )



from matplotlib.gridspec import GridSpec

year = 2013
def set_data():
        
    dn = dt.datetime(year, 1, 1, 20)
    
    df = b.sel_times(
        pb.concat_files(year), 
        dn, 
        hours = 11)
    
    long = -60
    return pb.longitude_sector(
        df, 
        long
        )


def plot_removing_bad_points(df):
    
    fig = plt.figure(
        figsize = (12, 5), 
        dpi = 300
        )
    plt.subplots_adjust(hspace = 0.2)
    
    gs = GridSpec(3, 3, figure=fig)
    
    ax1 = fig.add_subplot(gs[0, :])
    
    ax1.plot(df['roti'], **args)
    
    b.format_time_axes(ax1)
    
    ax1.set(title = f'Longitude: {long}°', 
            ylabel = 'ROTI' 
            )
    
    
    times = [dt.datetime(year, 1, 1, 20, 40), 
             dt.datetime(year, 1, 1, 23, 40), 
             dt.datetime(year, 1, 2, 3, 40)]
    
    ax2 = fig.add_subplot(gs[-1, 0])
    ax3 = fig.add_subplot(gs[-1, -2])
    ax4 = fig.add_subplot(gs[-1, -1])
    
    for i, ax in enumerate([ax2, ax3, ax4]):
        dn = times[i]
        plot_section(ax, df, dn, i = 1)
        
        

plot_removing_bad_points(df)