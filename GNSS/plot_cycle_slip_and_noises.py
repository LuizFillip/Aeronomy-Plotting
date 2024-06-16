import matplotlib.pyplot as plt 
import base as b 
import PlasmaBubbles as pb 
import datetime as dt
import pandas as pd


b.config_labels()


def load_data(dn, root = 'E:\\', sector = -50):
    
        
    out = []
    for day in range(2):
        delta = dt.timedelta(days = day)
    
        path = pb.path_roti(dn + delta, root = root)
        
        out.append(b.load(path))
        
    df = b.sel_times(pd.concat(out), dn, hours = 16)
    
    return pb.filter_region(df, dn.year, sector)
    
   



dn = dt.datetime(2013, 12, 24, 18)
df = load_data(dn)

# df = df.loc[df['sts'] == 'salu']
fig, ax = plt.subplots(
    nrows = 2,
    sharey = True, 
    sharex = True, 
    figsize = (10, 8)
    
    )

ax[0].plot(df['roti'])

ds = df.loc[df['el'] >  30]

ax[-1].plot(ds['roti'])

ax[-1].set(ylim = [0, 5])

b.format_time_axes(ax[-1])
 