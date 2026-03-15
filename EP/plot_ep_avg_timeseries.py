import GOES as gs 
import matplotlib.pyplot as plt 
import pandas as pd 

 
nuclei = []
waves = []
for year in range(2012, 2018):
    nuclei.append(gs.load_nuclei(year))
    
    waves.append(gs.load_ep_data(
        year = year,
        alt = None,
        ep_col = "Ep_mean"
    ))

 
nc = pd.concat(nuclei)
wv = pd.concat(waves)

#%%%%


def plot_ep_timeseries(ax, waves, alt):
    
    
    
    ds= gs.filter_space(
            waves,
            lon_min = lon_min,
            lon_max = lon_max,
            lat_min = lat_min,
            lat_max = lat_max,
        )
    
    ds = ds.loc[ds['alt'] == alt]
 
    daily_count = ds['Ep_mean'].resample("1D").mean()
    
    occ_month = daily_count.resample("MS").mean().sort_index()
    
    ax.plot(occ_month.index, occ_month.values,
            lw = 3, label = f'{alt} km')
    
    ax.legend()
 
    
    

def plot_nucleos_timeseries(ax, nucleo):
    ax1 = ax.twinx()
    

 
    ds = gs.filter_space(
            nucleo,
            lon_min = lon_min,
            lon_max = lon_max,
            lat_min = lat_min,
            lat_max = lat_max,
        )
    
    daily_count = ds.resample("1D").size()
    
    occ_month = daily_count.resample("MS").mean()
    
    ax1.plot(occ_month.index, occ_month.values,
             lw=3, color="blue")
        
    return occ_month 
  
    

lat_min = -20

lon_min = -70
lon_max = -40
 
lat_max = lat_min + 10
 
 
fig, ax = plt.subplots(
    figsize = (12, 8), 
    nrows = 2, 
    sharex = True
    )



plot_nucleos_timeseries(ax[0], nc)

for alt in range(20, 120, 20):
    
    
    plot_ep_timeseries(ax[1], wv, alt)