# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 17:47:49 2026

@author: Luiz
"""
def load_indices(dn):
    
    import core as c
    
    df = pb.longterm_raw_roti(dn, days = 3)

    ds = b.sel_times(df, dn, hours = 12) 
    
    ds =  ds.replace(9999.99, np.nan)
    
    return ds

def plot_epbs(ax, dn, sector = -50):
    
    df = pb.concat_files(
        dn, 
        days = 2, 
        root = 'E:\\', 
        hours = 12, 
        remove_noise = True
        )
    df = pb.filter_region(df, dn.year, sector)
    
    ax.plot(df['roti'])
    
    ax.set(ylim = [0, 2], ylabel = 'ROTI')
    
    return None 

def plot_one_day_indices(dn, days = 2):
    '''
    plot para os indices (a escolher)
    e ROTI - paper da estatistica de tempestade
    '''
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (14, 14), 
        nrows = 4, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
  
    ds = load_indices()
       
    plot_magnetic_fields(ax[0], ds)
    pl.plot_auroral(ax[1], ds)
    plot_dst(ax[2], ds)
   
    b.format_time_axes(
        ax[-1], 
        hour_locator = 1, 
        translate = True
        
        )
    
    delta = dt.timedelta(hours = 2)
    
    for a in ax.flat:
         
        dusk, midnight  = pl.plot_references_lines(
                a,
                -50, 
                dn, 
                label_top = None,
                translate = True
                )
        
        a.axvspan(
            dusk - delta,
            dusk + delta, 
            ymin = 0, 
            ymax = 1,
            alpha = 0.2, 
            color = 'gray'
            )
        
    res = ds.loc[
        (ds.index > dusk - delta) &
        (ds.index < dusk + delta)
        ]
    
    # print(res.mean())
    
    b.plot_letters(
        ax, 
        y = 0.8, 
        x = 0.03, 
        num2white = None
        )
    fig.align_ylabels()
    return fig 
