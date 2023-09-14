import datetime as dt
import base as b 
import matplotlib.pyplot as plt
import PlasmaBubbles as pb 

args = dict(marker = 'o', 
             markersize = 3,
             linestyle = 'none'
             )


def plot_epbs_occurrences_roti(ds):

    fig, ax = plt.subplots(
        nrows = 2, 
        dpi = 300, 
        sharex = True, 
        figsize = (10, 6)
        )
    
    b.config_labels()
    
    ds = ds[['-60', '-40', '-50']]
    
    plt.subplots_adjust(hspace = 0.1)
    
    color = ['k', 'b', 'r']
    
    for i, col in enumerate(ds.columns):
        
        the = pb.threshold(ds[col])
        
        line, = ax[0].plot(
            ds[col], label = f'{col}° ({the})', 
            color = color[i], 
            **args
            )
        
        
        ax[0].axhline(
            the, color = line.get_color()
            )
        
    
        ax[1].plot(
            pb.get_events(
                ds[col], 
                progress_bar = False
                ), 
            marker = 'o',
            markersize = 3,
            color = line.get_color(), 
            label = f'{col}° ({the})'
            )
    

    ax[0].set(
        ylim = [0, 4], 
        yticks = list(range(5)),
        ylabel = 'ROTI (TECU/min)'
        )
    
    ax[1].legend(
        ncol = 5, 
        title = 'Longitudinal zones and thresholds (TECU/min)',
        bbox_to_anchor = (.5, 2.6), 
        loc = "upper center"
        )
    
   
    ax[1].set(ylabel = 'EPBs occurence', 
              yticks = [0, 1], 
              ylim = [-0.2, 1.2])
    
     
    b.format_time_axes(ax[1])
    
    for limit in [0, 1]:
        ax[1].axhline(
            limit, 
            color = 'k', 
            linestyle = '--'
            )
    
    return fig


def save_img(df, dn, root):
    

    ds = b.sel_times(df, dn, hours = 10)
    
    plt.ioff()
        
    fig = plot_epbs_occurrences_roti(ds)
    
    FigureName = dn.strftime('%j.png')
    
    fig.savefig(root + FigureName,
                pad_inches = 0, 
                bbox_inches = "tight")
    
    plt.clf()   
    plt.close()
    
    

from tqdm import tqdm  


def save_year(year, root):
    

    b.make_dir(root)
    
    infile = f'database/EPBs/longs/{year}.txt'
    
    for day in tqdm(range(365), 
                    desc = str(year)):
        
        delta = dt.timedelta(days = day)
        
        dn = dt.datetime(year, 1, 1, 21) + delta
        
        df = b.load(infile)
        
        save_img(df, dn, root)
        
        
# for year in range(2013, 2023):
    
#     root = f'D:\\img\\{year}\\'
#     save_year(year, root)


year = 2013
infile = f'database/EPBs/longs/{year}.txt'
dn = dt.datetime(year, 6, 8, 21)

df = b.load(infile)

ds = b.sel_times(df, dn, hours = 10)

fig = plot_epbs_occurrences_roti(ds)

plt.show()