import matplotlib.pyplot as plt 
import os
import RayleighTaylor as rt 
import base as b 

def plot_compare_solar_activity(site = 'saa'):
    

    fig, ax = plt.subplots(
        sharey = True,
        dpi = 300, 
        nrows = 2,
        figsize = (14, 8), 
        )
    
    
    
    df = rt.load_grt(site)

   
    ds = df.loc[df.index.year == 2014]
    
    ds['ratio'].plot(ax = ax[0])

    ds = df.loc[df.index.year == 2019]
    
    ds['ratio'].plot(ax = ax[1])
    
plot_compare_solar_activity()