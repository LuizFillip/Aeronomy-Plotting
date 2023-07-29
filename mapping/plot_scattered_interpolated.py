from GEO import quick_map
import pandas as pd

fig, ax = quick_map()
infile = "database/GNSS/roti/2013/001.txt"
df = pd.read_csv(infile)

prns = df['prn'].unique()


for prn in prns:
    ds = df.loc[(df['prn'] == prn) &
                (df['sts'] == 'ceft')]
    
    ax.plot(ds['lon'], ds['lat'], lw = 2)

