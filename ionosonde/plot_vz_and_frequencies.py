import matplotlib.pyplot as plt
import digisonde as dg
import base as s
import datetime as dt 

s.config_labels(fontsize = 25)


def plot_vz_and_frequencies(df, vz, freqs = [5, 6, 7]):
    
    
    fig, ax = plt.subplots(
        figsize = (12, 8), 
        nrows = 2, 
        sharex = True, 
        dpi = 300
        )

    plt.subplots_adjust(hspace = 0.1)
    
    for num, col in enumerate(freqs):
        
        
        ax[0].plot(df[col], label = f'{col}')
        ax[1].plot(vz[col])


    ax[0].set(ylabel = "Altitude (km)", 
              ylim = [100, 500], 
              )

    ax[1].set(
              ylabel = r"Deriva vertical (m/s)", 
              ylim = [-50, 50], 
              xlim = [df.index[0], df.index[-1]]
              )
     
    s.format_time_axes(ax[1], translate = True)
    
    ax[0].legend(
        # bbox_to_anchor = (.5, 1.05), 
        ncol = 3, 
        loc = "upper right", 
        title = "Frequências fixas"
        )

    ax[1].axhline(0, linestyle = '--')
    
    s.plot_letters(ax, y = 0.85, x = 0.03)

    return fig

dn = dt.datetime(2013, 12, 24, 16)

FigureName = 'frequencies_and_drift'


infile = 'digisonde/data/FZA0M_20131224(358).TXT'
df = dg.freq_fixed(infile).interpolate()
 
df = s.sel_times(df, dn, hours = 10)

vz = dg.vertical_drift(df).interpolate()

fig = plot_vz_and_frequencies(df, vz)

fig.savefig(
    s.LATEX(FigureName, 
    folder = 'timeseries')
    )
