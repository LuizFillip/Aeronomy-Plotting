import epbs as pb 
import datetime as dt 


def plot_roti_in_range(
        ax, start, end, 
        root = 'F:\\', 
        clear = None, 
        lim = 0.3
        ):

    ds = pb.longterm_raw_roti(start, end, root = root)
    
    if clear is not None :
        delta = dt.timedelta(hours = 4)
        ds = ds.loc[
            ~((ds.index > clear) & 
            (ds.index < clear + delta)  & 
            (ds['roti'] > lim))]
        
        
    ax.scatter(
        ds.index, 
        ds['roti'], 
        c = 'k', 
        s = 5, 
        alpha = 0.6
        )
    
    ax.set(
        ylabel = 'ROTI\n(TECU/min)',
        ylim = [0, 5], 
        yticks = list(range(6)),
        
        )
    
  
    return ds
