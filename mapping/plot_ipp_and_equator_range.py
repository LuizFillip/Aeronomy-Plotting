from GEO import quick_map
from base import load

lat_lims = dict(min = -40, max = 10, stp = 10)

lon_lims = dict(min = -80, max = -30, stp = 10)    

fig, ax = quick_map(
    lat_lims = lat_lims, 
    lon_lims = lon_lims, 
    figsize = (5, 5)
    )

p = 'database/GNSS/roti/2014/001.txt'
df = load(p)

prns = df['prn'].unique()
stations = df['sts'].unique()

for sts in stations:
    for prn in prns:
        ds = df.loc[(df['prn'] == prn) &
                    (df['sts'] == sts)]
        
        ax.plot(ds['lon'], ds['lat'], lw = 2)
    
