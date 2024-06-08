import matplotlib.pyplot as plt
import digisonde as dg
import base as b 
import GEO as gg 
import plotting as pl 
import numpy as np

b.config_labels(fontsize = 25)
FREQ_PATH = 'digisonde/data/chars/freqs/'
CHAR_PATH = 'digisonde/data/chars/midnight/'



def plot_infos(ax, vz, site):

    data = dg.time_between_terminator(
        vz, site = site)

    ax.axvline(data['time'], label = 'Vp')
    
    time = data['time'].strftime('%Hh%M')
    
    vmax = round(data['vp'], 2)
    
    ax.text(
        0.4, 0.82,
        f'$V_p =$ {vmax} m/s',
        transform = ax.transAxes
        )
    
    ax.axhline(0, linestyle = '--')
    



def plot_heights(ax, df, cols):
    
    ax.plot(df[cols], label = cols)

    ax.set(
        ylabel = "Altitude (km)", 
        ylim = [100, 400])
    
 

def plot_drift(ax, vz, cols, site, vmax = 50):
    
    lb = pl.labels('en')
    
    ax.plot(vz[cols], label = cols)
    ax.set(
          ylabel = lb.vz, 
          ylim = [-vmax, vmax], 
          yticks = np.arange(-vmax, vmax + 10, 20),
          xlim = [vz.index[0], vz.index[-1]]
          )

    ax.axhline(0, linestyle = '--')
    plot_infos(ax, vz, site)


def plot_QF(ax, df):
    
    ax.bar(df.index, df["QF"],
           width = 0.009, alpha = 0.5)
    
    ax.set(
        ylim = [0, 80], 
        ylabel = "QF (Km)"
        )

    
def plot_vz_and_frequencies(df, vz, char, site):
    
    dn = df.index[0]

    fig, ax = plt.subplots(
        figsize = (12, 8), 
        nrows = 2, 
        sharex = True, 
        dpi = 300
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    cols = list(range(3, 7, 1))
    
    plot_heights(ax[0], df, cols)
    plot_drift(ax[1], vz, cols, site)
    b.format_time_axes(ax[1], translate = False)

    pl.plot_terminators(ax, dn)
    
    b.plot_letters(ax, y = 0.85, x = 0.03)
    
    ax[0].set(title = gg.sites[site]['name'])
    
    ax1 = ax[1].twinx()
    plot_QF(ax1, char)
    
    plt.show()

    return fig






def main():
    file = 'SAA0K_20170830(242).TXT'
    file = 'FZA0M_20220724(205).TXT'
    file = 'SAA0K_20130516(136).TXT'
    char = dg.chars(CHAR_PATH + file)
    
    ds, vz, site = pl.pipe_data(file)
#     fig = plot_vz_and_frequencies(ds, vz, char, site)
    
# main()


