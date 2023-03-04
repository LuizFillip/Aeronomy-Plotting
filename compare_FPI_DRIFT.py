from FabryPerot.core import FabryPerot
import matplotlib.pyplot as plt
import pandas as pd
import setup as s
from Digisonde.drift import load_export
import datetime as dt
from FabryPerot.fpi_utils import file_attrs

fig, ax = plt.subplots(ncols = 2, 
                       figsize = (16, 6), 
                       sharex = True, 
                       sharey = True)

plt.subplots_adjust(wspace = 0.05)

fpi_file = 'FabryPerot/database/2013/minime01_car_20130101.cedar.005.txt'
fpi_file = "FabryPerot/database/2013/minime01_car_20130625.cedar.005.txt"

fpi_file = "FabryPerot/database/2013/minime01_car_20131001.cedar.006.txt"

fpi_file = "FabryPerot/database/2013/minime01_car_20131116.cedar.007.txt"
df = FabryPerot(fpi_file).wind



date = file_attrs(fpi_file).date
year = date.year

coords = [("east", "west"), ("north", "south")]

for n, coord in enumerate(coords):

    dat = df.loc[(df["dir"] == coord[0]) | 
                 (df["dir"] == coord[1]), ["vnu"]]
    
    ax[n].plot(dat, label = "Fabry-Perot - Cariri")
    
s.format_axes_date(ax[0], time_scale = "hour")
  
drift_file = f"Digisonde/database/drift/SSA/{year}/{year}01.txt"

def load_drift2():
    drift_file = f"Digisonde/{year}_raw.txt"

    ts = pd.read_csv(drift_file, index_col = 0)

    ts.index = pd.to_datetime(ts.index)
    
    return ts

ts = load_export(drift_file)

ts = load_drift2()

b = date + dt.timedelta(hours = 21)
e = b + dt.timedelta(hours = 11)

ts = ts.loc[(ts.index >= b) & (ts.index <= e)]

ts["vx"].plot(ax = ax[1], 
              yerr = ts["evx"], 
              label = "Drift-X - São Luis")
ts["vy"].plot(ax = ax[0], 
              yerr = ts["evy"], 
              label = "Drift-X - São Luis")

na = ["zonal", "meridional"]

hwm_file = f"FabryPerot/database/HWM/saa_250_{year}.txt"

df = pd.read_csv(hwm_file, index_col = "time")

df.index = pd.to_datetime(df.index)

df = df.loc[(df.index >= b) & (df.index <= e)]

for n, ax in enumerate(ax.flat):
    
    ax.plot(df[na[n][:3]], 
            label = "HWM-14 - São Luis")
    ax.axhline(0, color = "k")
    ax.legend()
    
    ax.set(title = na[n], 
           xlabel = "Hora universal (UT)",
           ylabel = "Velocidade (m/s)")

fig.suptitle(f"{b.strftime('%d/%m/%Y')}")
fig.autofmt_xdate(rotation = 0, ha = 'center')