import PlasmaBubbles as pb 
import GEO as gg 

def plot_terminator_and_midnight(
        ax, 
        dn,
        ref_long = -50,  
        vmax = 4, 
        translate = False,
        midnight = True
        ):
    
    dusk = pb.terminator(ref_long, dn, float_fmt = False)
    
    ax.axvline(dusk, lw = 2)
    
    midnight = gg.local_midnight(
        dn, ref_long + 5, delta_day = 1)
    
    ax.axvline(midnight, lw = 2, color = 'b')
    
    y = vmax + 1.1
    
    if translate:
       term_label = 'Terminator (300 km)'
       midn_label = 'Local midnight'
    else:
       term_label = 'Terminadouro (300 km)'
       midn_label = 'Meia noite local'
    
    ax.text(
        dusk, y, term_label, 
        transform = ax.transData
        )
        
    if midnight:
        ax.text(
            midnight, y, midn_label, 
            color = 'b',
            transform = ax.transData)