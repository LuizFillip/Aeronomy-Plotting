import GNSS as gs 
import datetime as dt 
import base as b 
import PlasmaBubbles as pb 
import matplotlib.pyplot as plt 
import pandas as pd 


date = dt.date(2015, 12, 20)

# days = c.undisturbed_days(date, threshold = 18).index 

salu = []
naus = []
cruz = []
pbjp = []
for day in range(351, 359, 1):
    
    path = gs.paths(2015, day).fn_roti()
    
    df = pb.load_filter(path, 
    remove_noise = False)
    
    salu.append(df.loc[df['sts'] == 'salu'])
    naus.append(df.loc[df['sts'] == 'naus'])
    cruz.append(df.loc[df['sts'] == 'cruz'])
    pbjp.append(df.loc[df['sts'] == 'pbjp'])
    
    
dsalu = pd.concat(salu)
dnaus = pd.concat(naus)
dcruz = pd.concat(cruz)
dpbjp = pd.concat(pbjp)



fig, ax = plt.subplots(
    figsize = (12, 10), 
    dpi = 300, 
    nrows = 3,
    sharex = True, 
    sharey = True
    )

names = ['SALU', 'NAUS', 'CRUZ', 'PBJP']
for i, ds in enumerate([dsalu, dnaus, dcruz]):
    
    ax[i].plot(ds['roti'])
    
    ax[i].text(
        0.05, 0.8, 
        names[i], 
        transform = ax[i].transAxes
        )
    
    ax[i].set(
        ylabel = 'ROTI (TECU/min)', 
        xlim = [ds.index[0], ds.index[-1]]
        )

b.format_days_axes(ax[-1])