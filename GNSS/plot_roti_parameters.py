import matplotlib.pyplot as plt
import GNSS as gs
import base as b
import datetime as dt
import numpy as np


b.config_labels(fontsize = 30)

    

def plot_rot(ax, tec, prn):
    stec = tec[prn]
    ds = gs.rot_from_stec(stec, tec.index)

    ax.axhline(0, color = 'k', linestyle = '--')
    ax.plot(ds['drot'])
    
    ax.set(ylabel = "ROT (TECU/min)", 
           ylim = [-12, 12], 
           yticks = np.arange(-10, 15, 5)
           )
    return None 
    
        
def plot_roti(ax, path, prn, station = 'salu'):
    
    df = b.load(path.fn_roti())
    
    df = df.loc[(df['sts'] == station) & 
                (df['prn'] == prn)]
    
    ax.plot(df['roti'])
    
    ax.set(
        ylim = [0, 5], 
        yticks = np.arange(0, 6, 1),
        ylabel = "ROTI (TECU/min)"
        )
    
    return df['el']

def plot_stec(ax, path, station, prn):
    
    tec = b.load(path.fn_tec(station))
    
    ax.plot(tec[prn].dropna())
    
    ax.set(
        ylabel = "STEC (TECU)", 
        xlim = [dt.datetime(2013, 12, 24, 20), 
                dt.datetime(2013, 12, 25, 0)], 
                yticks = np.arange(50, 250, 50)
        )
    return tec


def plot_elevation(ax, el):
    ax.plot(el)

    ax.set(ylabel = 'Elevação (°)', 
           ylim = [20, 60], 
           yticks = np.arange(20, 70, 10))


def plot_shades(ax, start, end):
    
    ax.axvspan(
        start, end,
        alpha = 0.2, 
        color = 'gray',
        edgecolor = 'k', 
        lw = 2
    )
    
    
    return None 

def plot_roti_parameters(dn, station, prn):
    
    fig, ax = plt.subplots(
        figsize = (12, 14),
        dpi = 300,
        nrows = 3,
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    doy = gs.doy_from_date(dn)
    
    path = gs.paths(dn.year, doy, root = 'E:\\')
    
    tec = plot_stec(ax[0], path, station, prn)
    
    plot_rot(ax[1], tec, prn)
    
    plot_roti(ax[2], path, prn)
    
    # plot_elevation(ax[0], el)
    ax[0].set(
        title = f'Estação: {station.upper()} - PRN: {prn}')
    
    b.format_time_axes(ax[-1], pad = 70)
    
    b.plot_letters(ax, y = 0.8, x = 0.02)
    
    for i, ax in enumerate(ax.flat):
        end = dt.datetime(2013, 12, 25, 0)
        start =  dt.datetime(2013, 12, 24, 22, 35)
        plot_shades(ax, start, end)
        
        if i == 0:
            d1 = dt.timedelta(hours = 1.5)
            ax.text(start - d1, 150, 'Sem EPBs', 
                    transform = ax.transData)
            
            d1 = dt.timedelta(minutes = 20)
            ax.text(start + d1, 150, 'Com EPBs', 
                    transform = ax.transData)
        
    return fig

def main():
    
    prn = 'G21'
    station = 'salu'
    dn = dt.datetime(2013, 12, 24)
        
    fig = plot_roti_parameters(dn, station, prn)
    
    FigureName = 'ROTI_parameters'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'timeseries'),
        dpi = 400
        )
    
# main()