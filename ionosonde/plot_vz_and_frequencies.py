import matplotlib.pyplot as plt
import digisonde as dg
import base as b 
import GEO as gg 
import datetime as dt


b.config_labels(fontsize = 25)
FREQ_PATH = 'digisonde/data/chars/freqs/'
CHAR_PATH = 'digisonde/data/chars/midnight/'

def plot_terminators(ax, dn):
         
     dusk = gg.dusk_from_site(
             dn, 
             site = 'saa',
             twilight_angle = 18
             )
     
     delta = dt.timedelta(minutes = 60)
     
     for row in range(2):
         
         # ax[row].axvspan(
         #     dusk - delta,
         #     dusk + delta,
         #     alpha = 0.2, 
         #     color = 'gray',
         #     lw = 2
         # )
             
         ax[row].axvline(
             dusk, 
             linestyle = '-',
             lw = 2,
             color = 'k'
             )
 

     return dusk

def plot_infos(ax, vz, site):

    data = dg.time_between_terminator(
        vz, site = site)

    ax.axvline(data['time'], label = 'Vp')
    
    time = data['time'].strftime('%Hh%M')
    
    vmax = round(data['vp'], 2)
    
    ax.text(
        0.55, 0.82,
        f'$V_p =$ {vmax} m/s ({time} UT)',
        transform = ax.transAxes
        )
    
    ax.axhline(0, linestyle = '--')
    

class labels:
    
    def __init__(self, language = 'pt'):
        if language == 'pt':
            self.vz = "Deriva vertical (m/s)"
            self.freq = 'Frequências fixas'
        else:
            self.vz = 'Vertical drift (m/s)'
            self.freq = 'Fixed frequencies'



def plot_heights(ax, df, cols):
    
    ax.plot(df[cols], label = cols)

    ax.set(
        ylabel = "Altitude (km)", 
        ylim = [100, 700])
    
    ax.legend(
        ncol = 2, 
        loc = "upper right", 
        title = 'Frequencies (MHz)'
        )

def plot_drift(ax, vz, cols, site, vmax = 70):
    
    lb = labels('en')
    
    ax.plot(vz[cols])
    ax.set(
          ylabel = lb.vz, 
          ylim = [-vmax, vmax], 
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
    
    cols = df.columns[3:-3]
    
    plot_heights(ax[0], df, cols)
    plot_drift(ax[1], vz, cols, site)
    b.format_time_axes(ax[1], translate = False)

    plot_terminators(ax, dn)
    
    b.plot_letters(ax, y = 0.85, x = 0.03)
    
    ax[0].set(title = gg.sites[site]['name'])
    
    ax1 = ax[1].twinx()
    plot_QF(ax1, char)
    
    plt.show()

    return fig





def pipe_data(file):
    df = dg.freq_fixed(FREQ_PATH + file)
    del df[9]
    site, dn = dg.site_datetime_from_file(file, hours = 18)
    
    ds = b.sel_times(df, dn, hours = 12).interpolate()
    
    ds = ds.iloc[1:]
    vz = dg.vertical_drift(ds)
    
    vz = vz.replace(0, float('nan'))
    
    return ds, vz, site

def main():
    file = 'SAA0K_20170830(242).TXT'
    file = 'FZA0M_20220724(205).TXT'
    char = dg.chars(CHAR_PATH + file)
    
    ds, vz, site = pipe_data(file)
    
    fig = plot_vz_and_frequencies(ds, vz, char, site)
    
main()