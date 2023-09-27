import GNSS as gs
import base as b 
import matplotlib.pyplot as plt 
import PlasmaBubbles as pb

def sel_single_station(path, station):

    df = b.load(path.fn_roti).sort_index()
    
    df = df[~df['prn'].str.contains('E')]
    
    ds = df.loc[df['sts'] == station]
         
    return pb.time_dataset(ds, 'roti', pb.time_range(df))



def plot_roti_scatter(ds1, station):
    
    b.config_labels()
    
    fig, ax = plt.subplots(
        figsize = (10, 5))
    
    names = 'GPS, GLONASS'
    
    ax.scatter(ds1.index, 
               ds1['roti'], 
               s = 5,
               color = 'k',
               label = names)
    
    ax.set(ylim = [0, 5], 
           ylabel = 'ROTI (TECU/min)', 
           title = station, 
           xlim = [ds1.index[0], ds1.index[-1]])
    
    b.format_time_axes(ax, hour_locator = 3)
    
    ax.legend(loc  = 'upper right')
    
    return fig


def run_all(station = 'ceft'):

    for doy in range(1, 366, 1):
                
        path = gs.paths(2021, doy)
        
        df = sel_single_station(path, station)
        fig = plot_roti_scatter(df, station)
        
        save_in = f'D:\\{station}\\{path.doy}.png'
        print('saving', doy)
        fig.savefig(save_in)


