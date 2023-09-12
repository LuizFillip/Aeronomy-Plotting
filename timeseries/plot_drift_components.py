import matplotlib.pyplot as plt
import datetime as dt
import base as b


def plot_drift_components(ts):
    
    """
    Vz: Vertical component (positive to up)
    Vx: Meridional component (positive to north)
    Vy: Zonal component (positive to east)
    """

    fig, ax = plt.subplots(
        nrows = 3, 
        dpi = 300, 
        sharex = True, 
        figsize = (12, 10)
        )
    
    plt.subplots_adjust(hspace = 0.2)
    b.config_labels()
    
    date = ts.index[0].strftime("%d de %B de %Y")
    
    args = dict(marker = "o", 
                linestyle = "none", 
                markersize = 5, 
                color = "k", 
                fillstyle = "none",
                capsize = 3)
    
    li = [100, 150, 150]
    na = ["vertical", "meridional", "zonal"]
    co = ["vz", "vx", "vy"]
    
    
    for n, ax in enumerate(ax.flat):
        
        ts[co[n]].plot(
            ax = ax, yerr = ts["e" + co[n]], **args)
        
        ax.axhline(0, color = "red")
        
        ax.set(ylim = [-li[n], li[n]], 
               xlim = [ts.index[0], 
                       ts.index[-1]], 
               ylabel = "Velocidade (m/s)")
        
        ax.grid()
        
        ax.text(0, 1.04, "Componente " + na[n], 
                transform = ax.transAxes)
        
        
        if n == 2:
            b.format_time_axes(ax)
            ax.set(xlabel = "Hora universal (UT)")
    
    fig.autofmt_xdate(rotation = 0, ha = 'center')
    fig.suptitle(date, y = 0.91)

def main():
    
    infile = 'digisonde/data/drift/data/saa/2016_drift.txt'
    
    df = b.load(infile)
    dn = dt.datetime(2016, 11, 19, 18)
    ts = b.sel_times(df, dn, hours = 12)
    
    plot_drift_components(ts)