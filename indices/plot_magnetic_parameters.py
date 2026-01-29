import base as b 
import core as c 
import numpy as np 

def plot_auroral(
        ax, 
        ds, 
        vmax = 3000, 
        step = 1000
        ):
    ax.plot(ds['ae'], lw = 1.5)
    ax.set(
        ylim = [0, vmax],
        yticks = np.arange(0, vmax + step, step),
        ylabel = 'AE (nT)'
        )
    return None


def plot_SymH(
        ax, ds, 
        ylim = [-300, 50], 
        kp = True, 
        color = 'red',
        step = 50
        ):
    
    ax.plot(ds, lw = 2, color = color)
   
    ax.set(
        xlim = [ds.index[0], ds.index[-1]], 
        ylim = [ylim[0], ylim[-1]],
        yticks = np.arange(ylim[0], ylim[-1] + step, step ),
        ylabel = "SYM-H (nT)"
        )
       
    for line in [0, -30, -50, -100]:
        ax.axhline(
            line, 
            lw = 0.5, 
            color = 'k', 
            linestyle = ':'
            )
        

    return None 



def plot_solar_speed(ax, ds, vmax = 800, step = 200):
    ds = ds.loc[ds['speed'] < 600]
    ax.plot(ds['speed'], lw = 1.5)
    ax.set(
        ylim = [300, vmax],
        yticks = np.arange(300, vmax + step, step),
        ylabel = '$V_{sw}$ (km/s)'
        )
    return None


def plot_electric_field(ax, ds):
    ds = ds.loc[ds['electric'] < 100]
    ax.plot(ds['electric'], lw = 1.5)
    ax.axhline(0, lw = 1, linestyle = ':')
    ax.set(
        ylabel = 'Ey (mV/m)', 
        ylim = [-15, 15]
        )
    return None 
 
    
 
def plot_dst(
        ax, ds, 
        ylim = [-150, 50], 
        color = 'k'):

    ax.plot(ds['sym'], lw = 1.5, color = color)
    
    ax.set(
        xlim = [ds.index[0], ds.index[-1]], 
        ylim = [ylim[0] - 30, ylim[-1]],
        yticks = np.arange(ylim[0], ylim[-1] - 30, 50),
        ylabel = "SYM-H (nT)"
        )
    
    ax.axhline(0, lw = 1, color = 'k', linestyle = '-')
    
    for limit in [-50, -150]:
        ax.axhline(
            limit, 
            lw = 1, 
            color = 'k', 
            linestyle = '--'
            )
    return None 
        

def plot_magnetic_fields(
        ax, 
        ds, 
        ylim = 30, 
        by = False, 
        ax_co = 'purple'
        ):
    
    ax.plot(
        ds['bz'], 
        label = '$B_z$', 
        lw = 2
        )
    
    ax.set(
        ylim = [-ylim, ylim], 
        yticks = np.arange(-30, 40, 15),
        ylabel = '$B_y$ (nT)' #'$Ey$ (mV/m)'
        )
    
    ax.axhline(0, lw = 1, linestyle = '--', color = 'k')
    
    if by:
        ax1 = ax.twinx()
        
        ax1.plot(
            ds['by'], 
            color = ax_co, 
            label = '$B_y$', 
            lw = 2
            )
        
        b.change_axes_color(
                ax1, 
                color = ax_co,
                axis = "y", 
                position = "right"
                )
         
        
    ax.set(
        ylabel = '$B_z$ (nT)',
        yticks = np.arange(-30, 40, 15),
        ylim = [-ylim - 5, ylim + 5]
        )
     
    return None 


def plot_kp_by_range(
        ax, dn, before = 4, forward = 4
        ):
    
    ds = b.range_dates(
        c.low_omni(), dn, 
        b = before, 
        f = forward
        )
    ds = ds.resample('3H').mean() 
    
    ax.bar(
        ds.index, 
        ds['kp'] / 10, 
        width = 0.1,
        color = 'gray', 
        alpha = 0.5
        )
    ax.set(
        ylabel = 'Kp', 
        ylim = [0, 12], 
        yticks = np.arange(0, 12, 2)
        )
    
    ax.axhline(3, lw = 2, color = 'r')
    return None 
