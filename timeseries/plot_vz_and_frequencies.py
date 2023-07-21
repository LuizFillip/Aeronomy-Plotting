import matplotlib.pyplot as plt
import digisonde as dg
import settings as s
from common import plot_terminators
from utils import smooth2

    
def plot_vz_and_frequencies():
    
    infile = "database/Digisonde/SAA0K_20130316(075)_freq"

    df = dg.fixed_frequencies(infile)

    vz = dg.drift(df)
    freqs = [5, 6, 7]

    for col in freqs:
        df[col] = smooth2(df[col], 5)
        vz[col] = smooth2(vz[col], 5)
        
        
    fig, ax = plt.subplots(
        figsize = (12, 7), 
        nrows = 2, 
        sharex = True, 
        dpi = 300
        )

    plt.subplots_adjust(hspace = 0.3)


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


    infile = "database/Drift/SSA/PRO_2013.txt"

    dig = dg.load_drift(infile)

    dig = dig[(dig.index > df.index[0]) & 
         (dig.index < df.index[-1]) ]

    ax[1].plot(dig["vz"], label = "DRIFT-X")

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
        
        plot_terminators(ax, df)
        ax.text(0.01, 1.1, f'({c[i]})', transform = ax.transAxes)
        
      
    return fig


#fig = plot_vz_and_frequencies()



# fig.savefig("digisonde/src/figures/vz_drift_heights.png", dpi = 300)
