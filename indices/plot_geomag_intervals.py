import base as b
import matplotlib.pyplot as plt 

def test_plot(ds, sections, dn):
    
    
    b.sci_format(fontsize = 25)
 
    fig, ax = plt.subplots(dpi = 200, figsize = (10, 5))
    
    ax.plot(ds['sym'])
    ax1 = ax.twinx()
    
    ax1.plot(ds['bz'], color = 'blue')
    b.change_axes_color(
            ax1, 
            color = 'blue',
            axis = "y", 
            position = "right"
            )
    for d in sections:
        ax.axvline(d, color = 'red')
    
    for ref_line in [0, -30, -50]:
        ax.axhline(ref_line, linestyle = '--')
  
    dusk = gg.terminator(-50, dn, float_fmt = False)
    
    ax.axvline(dusk, linestyle = '--', color = 'b', lw = 3)
    ax.set(
        ylabel = 'Sym/h (nT)',
        xlabel = 'Days',
        title = dn.strftime('%B, %Y')
        )
        
    ax1.set(ylim = [-30, 30], ylabel = 'Bz (nT)')
    b.format_days_axes(ax) 
    
    return None
    