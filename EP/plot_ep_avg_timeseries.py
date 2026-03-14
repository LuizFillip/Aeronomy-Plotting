import GOES as gs 
import matplotlib.pyplot as plt 

df = gs.potential_energy(year = 2013)

# dn = dt.date(2013, 2, 1)
# df = df.loc[df.index.date == dn]
    
# plot_dialy_Ep_points(df, step = 4)

df = gs.filter_space(
        df, 
        lon_min = -60, 
        lon_max = -40, 
        lat_min = -10, 
        lat_max = 0
        )

values = 'mean_90_110'
df = df.resample('1D').max().interpolate()
df[values].plot()