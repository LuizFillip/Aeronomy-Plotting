import matplotlib.pyplot as plt 
import base as b 
import PlasmaBubbles as pb 
import datetime as dt

b.config_labels(fontsize = 25)

def load_dataset(dn, hours = 12):
    
    out = []
    for folder in [ 'events2', 'long2']:
        ds = b.load(
            pb.epb_path(
                dn.year, root = 'D:\\', folder = folder)
            )
        
        out.append(b.sel_times(ds, dn, hours = hours))
        
    return tuple(out)


def plot_roti_epb_occurrence_in_column(df, ds):
    
    fig, ax = plt.subplots(
        nrows = 4,
        ncols = 2, 
        dpi = 300, 
        sharey= 'col',
        sharex= True,
        figsize = (18, 10)
        )

    plt.subplots_adjust(hspace = 0.05)

    dn = df.index[0]
    
    for i, col in enumerate(df.columns):
    
        ax[i, 0].plot(df[col])
        ax[i, 1].plot(ds[col])
        
        ax[i, 0].axhline(0.25, lw = 2, color = 'r')
        
        terminator = pb.get_term(int(col), dn, float_fmt = False)
        
        ax[i, 1].axvline(terminator, color = 'k', lw = 2)
        ax[i, 0].axvline(terminator, color = 'k', lw = 2)
        
        ax[i, 0].text(
            0.1, 0.85, col, 
            transform = ax[i, 0].transAxes
            )
    
        ax[i, 0].set(ylim = [0, 4])
        
    b.format_time_axes(ax[-1, 0])
    b.format_time_axes(ax[-1, 1])
    
    return fig 


dn = dt.datetime(2013, 5, 15, 20)

ds, df = load_dataset(dn, hours = 12)

fig = plot_roti_epb_occurrence_in_column(df, ds)