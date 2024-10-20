import base as b
import PlasmaBubbles as pb 
import GEO as gg
import numpy as np 
import digisonde as dg 
import datetime as dt 

b.config_labels()



def plot_occurrence_events(
        ax, 
        ds,
        threshold = 0.25,
        color = 'b', 
        false_filter = None
        ):
    
    ev = pb.events_by_longitude(ds['max'], threshold)
    
    if false_filter is not None:
        ev.loc[ev.index < false_filter] = 0
        
    line, = ax.plot(
          ev, 
          marker = 'o',
          markersize = 3,
          color = 'b'
        )
    
    b.change_axes_color(
            ax, 
            color = 'b',
            axis = "y", 
            position = "right"
            )
    
    ax.set(
        yticks = [0, 1], 
        xlim = [ds.index[0], ds.index[-1]],
        ylim = [-0.2, 1.4]
        )
    
    for limit in [0, 1]:
        ax.axhline(
            limit, 
            color = color, 
            linestyle = '--'
            )
        
    return ev
        




def plot_references_lines(
        ax,
        ref_long, 
        start, 
        label_top = None,
        translate = True
        ):
    
    if translate:
        term_name = 'Local terminator'
        midn_name = 'Local midnight'
    else:
        term_name = 'Terminadouro local'
        midn_name = 'Meia-noite local'
    
    dusk = gg.terminator(
        ref_long, 
        start, 
        float_fmt = False
        )
    
    ax.axvline(dusk, lw = 2)
    
    midnight = gg.local_midnight(
        start, 
        ref_long + 5, 
        delta_day = 1
        )
    
    ax.axvline(
        midnight, 
        lw = 2,
        color = 'k',
        linestyle = '--'
        )
    
    if label_top is not None:
        ax.text(
            dusk, label_top,
            term_name,
            transform = ax.transData
            )

        ax.text(
            midnight, label_top,
            midn_name,
            transform = ax.transData
            )
    
    return dusk, midnight 

def plot_lines( 
        axes, 
        start,  
        plot_term = False,
        y = 4.8, 
        label_top = None, 
        st = 0
        ):
    """
    Plot terminator of the first occurrence in 
    the region and find the local midnight 
    
    """
    
    sectors = np.arange(-80, -40, 10)[::-1]
    
    for i, ax in enumerate(axes[st:]):
        
        # if i == 0:
        #     label_top = 5.5
        # else:
        #     label_top = None
        dusk, midnight = plot_references_lines(
            ax, 
            sectors[i], 
            start, 
            label_top = label_top
            )
     
    return None
 
def plot_vertical_drift(
        ax, 
        dn, 
        target, 
        site, 
        vmax = 80, 
        hours = 12
        ):
    
    cols = list(range(5, 8, 1))
    
    file = dn.strftime(f'{site}_%Y%m%d(%j).TXT')

    ds = dg.IonoChar(file, cols)
    
    df = b.sel_times(ds.drift(smooth = 5), dn, hours)
    ds1 = df.loc[df.index < target]
    ax.plot(ds1['vz'], lw = 2)
    
    pre = round(df['vz'].max(), 2)
    
    ax.text(
        0.72, 0.75, 
        '$V_{zp} =$' + f'{pre} m/s', 
        transform = ax.transAxes
        )
    
    ax.set(
        ylabel = 'Vz (m/s)',
        ylim = [-vmax + 20, vmax], 
        yticks = np.arange(-vmax + 20, vmax + 10, 40), 
        xlim = [df.index[0], df.index[-1]],
        xticklabels = []
        )
    
    plot_references_lines(ax, -50, dn, label_top = vmax + 6)
    
    s = f'(a) {ds.site} ionosonde'
    ax.text(0.01, 0.8, s, transform = ax.transAxes)

    ax.axhline(0, linestyle = '--')
    
    ax1 = ax.twinx()
    
    df =  b.sel_times(ds.chars , dn, hours)
    ds = df.loc[df.index < target]
    ax1.bar(
        ds.index, 
        ds["QF"],
        width = 0.01, 
        color = 'gray',
        alpha = 0.7,
        )
    ylim = [0, 100]
    ax1.set(
        ylim = [ylim[0], ylim[-1]], 
        yticks = np.arange(ylim[0], ylim[-1] + 20, 30),
        ylabel = "QF (Km)", 
        xticklabels = []
        )
    
    return None

def plot_roti_timeseries(
        axes, 
        df, 
        target, 
        dn,  
        site, 
        right_ticks = False, 
        vmax  = 2, 
        threshold = 0.25,
        occurrence = True,
        plot_drift = True , 
        translate = True
        ):
        
    sectors = np.arange(-80, -40, 10)[::-1]    
    
    
    if plot_drift:
        plot_vertical_drift(axes[0], dn, target, site)
        st = 1
    else:
        st = 0
    
    plot_lines(axes, dn, y = vmax + 1.2, st = st)
    
    for i, ax in enumerate(axes[st:]):
             
        sel = pb.filter_region_and_dn(df, target, sectors[i])
        
        plot_roti_points(
            ax, sel, 
            threshold,
            label = False, 
            points_max = True,
            vmax = vmax,
            occurrence = occurrence
            )
        
        l = b.chars()
        s = f'({l[i + st]}) Box {i + 1}'
        ax.text(
            0.01, 0.8, s, 
            transform = ax.transAxes
            )
        
        ax.set(
            ylim = [0, vmax + 2], 
            yticks = list(range(0, vmax + 3, 2)), 
            xlim = [df.index[0], df.index[-1]], 
            )
        
        if right_ticks:
            ax.tick_params(
                axis='y', 
                labelright = True, 
                labelleft = False, 
                right = True, 
                left = False
                )
            
        if i != -1:
            ax.set(xticklabels = [])
            
    
    
    axes[0].set(xlim = axes[1].get_xlim())
    b.format_time_axes(axes[-1], translate = translate)
    
    return None 


