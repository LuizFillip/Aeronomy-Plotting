import matplotlib.pyplot as plt
import datetime as dt
import base as b


def plot_drift_components(ts, co):
    
    """
    Vz: Vertical component (positive to up)
    Vx: Meridional component (positive to north)
    Vy: Zonal component (positive to east)
    """
    
    na = ["vertical", "meridional", "zonal"]

    fig, ax = plt.subplots(
        nrows = len(na), 
        dpi = 300, 
        sharex = True, 
        figsize = (12, len(co) * 3)
        )
    
    plt.subplots_adjust(hspace = 0.2)

    
    
    li = [100, 150, 150]
    
    
    
    

dn = dt.datetime(2018, 2, 13, 0)

infile = f'digisonde/data/drift/data/saa/{dn.year}_drift.txt'

df = b.load(infile)

# ts = b.sel_times(df, dn, hours = 24)

ts = df.loc[df.index.date == dn.date()]

fig, ax = plt.subplots(
    dpi = 300, 
    sharex = True, 
    figsize = (12, 4)
    )

date = ts.index[0].strftime("%d de %B de %Y")

args = dict(
    marker = "o", 
    linestyle = "none", 
    markersize = 5, 
    color = "k", 
    fillstyle = "none",
    capsize = 3
    )

co = "vz"

lim = 50
ts[co].plot(ax = ax, yerr = ts["e" + co], **args)

ax.axhline(0, color = "red")

ax.set(ylim = [-lim, lim], 
       xlim = [ts.index[0], ts.index[-1]], 
       ylabel = "Velocidade (m/s)")
        
ax.axhline(40, color = 'red', linestyle = '--')

b.format_time_axes(
        ax, 
        translate = True,
        hour_locator = 2)

fig.autofmt_xdate(rotation = 0, ha = 'center')
fig.suptitle(date, y = 0.91)