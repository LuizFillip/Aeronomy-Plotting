import matplotlib.pyplot as plt
import digisonde as dg
import base as s
import datetime as dt 
    
def plot_vz_and_frequencies(dn):
    
    infile = 'digisonde/data/fixed_frequencies/SL_2014-2015/SAA0K_201401.txt'
    df = dg.freq_fixed(infile).interpolate()
   
    df = s.sel_times(df, dn, hours = 10)
    vz = dg.vertical_drift(df)
    # vz = vz.iloc[-1:]
    freqs = [5, 6, 7]

        
    fig, ax = plt.subplots(
        figsize = (10, 7), 
        nrows = 2, 
        sharex = True, 
        dpi = 300
        )

    plt.subplots_adjust(hspace = 0.05)
    
    for num, col in enumerate(freqs):
        ax[1].plot(vz[col])
        ax[0].plot(df[col], label = f'{col}')


    ax[0].set(ylabel = "Altitude (km)", 
              ylim = [100, 500], 
              )

    ax[1].set(
              ylabel = r"Deriva vertical (m/s)", 
              ylim = [-50, 50], 
               xlim = [df.index[0], df.index[-1]]
              )
     
    s.format_time_axes(ax[1])
    
    ax[0].legend(
        bbox_to_anchor = (.3, 1.), 
        ncol = 3, 
        loc = "lower left", 
        title = "Frequências fixas"
        )

    ax[1].legend(loc = "upper right")
    c = s.chars()
    s.config_labels(fontsize = 20)

    for i, ax in enumerate(ax.flat):
        
        ax.text(0.01, 0.85, f'({c[i]})', 
                transform = ax.transAxes)
        
      
    return fig

dn = dt.datetime(2014, 1, 1, 16)
fig = plot_vz_and_frequencies(dn)


fig.savefig(s.LATEX('frequencies_and_drift', 
                    folder = 'timeseries'))
