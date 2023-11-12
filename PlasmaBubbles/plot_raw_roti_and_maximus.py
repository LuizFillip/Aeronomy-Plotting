import matplotlib.pyplot as plt 
import base as b
import datetime as dt  
import os 
import PlasmaBubbles as pb 



def load_receivers(dn):
    
    df = pb.concat_files(
        dn, 
        pb.load_filter, 
        root = os.getcwd()
        )
    
    ds = b.sel_times(df, dn, hours = 12)
    
    receivers = [
        'pepe',
         'mabb',
         'mabs',
         'crat',
         'topl',
         'maba',
         'pitn',
         'picr',
         'brft',
         'ceft',
         'ceeu',
         'salu',
         'impz'
         ]
        
    return ds.loc[ds['sts'].isin(receivers)]

args = dict(
     marker = 'o', 
     markersize = 3,
     linestyle = 'none', 
     color = 'gray', 
     alpha = 0.2, 
     )
    


def plot_roti_curves(ax):
    
    ds = b.load('roti2.txt')
    
    ax.plot(ds['roti'], **args, 
            label = 'ROTI points')
    
    times = pb.time_range(ds)
    
    ax.axhline(0.25, color = 'red', lw = 2, 
                label = '0.25 TECU/min')
    
    df1 = pb.time_dataset(
        ds, 
        'max', 
        times
        )
    
    ax.plot(df1, 
            color = 'k',
            marker = 'o', 
            markersize = 3, 
            linestyle = 'none',
            label = 'Maximum value')
    
    ax.set(yticks = list(range(0, 4)), 
           ylabel = 'ROTI (TECU/min)')
    ax.legend(loc = 'upper right')
    
    b.format_time_axes(ax)

# day = df.between_time(
#     '12:00', '20:00'
#     )

# avg = day['roti'].mean()
# std = day['roti'].std()

# avg * 1.4 + std * 4


# def plot_raw_roti_and_maximus():
    
# fig, ax = plt.subplots(
#     dpi = 300, 
#     figsize = (10, 4)
#     )

dn = dt.datetime(2013, 6, 10, 20)



# plot_raw_roti_and_maximus()
# ds = load_receivers(dn)

# ds.to_csv('roti2.txt')