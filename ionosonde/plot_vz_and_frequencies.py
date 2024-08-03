import matplotlib.pyplot as plt
import digisonde as dg
import base as b 
import GEO as gg 
import datetime as dt 
import numpy as np

b.config_labels(fontsize = 30)


def plot_infos(ax, vz, site = 'saa'):
    
    dn = vz.index[0]
    
    data = dg.get_infos(vz, dn, site = 'saa')
    
    ax.axvline(data['time'], label = 'Vp')
    
    time = data['time'].strftime('%Hh%M UT')
    
    vmax = round(data['vp'], 2)
    vmax = str(vmax).replace('.', ',')
    ax.text(
        0.55, 0.83,
        f'$V_{{zp}} =$ {vmax} m/s ({time})',
        transform = ax.transAxes
        )
    
    return None 



def plot_heights(ax, df, cols):
   
    ax.plot(df[cols], label = cols, lw = 1.5)

    ax.set(
        ylabel = "Altitude (km)", 
        ylim = [100, 600])
    
    return None 

def plot_drift(ax, df, cols, site, vmax = 60):
        
    ax.plot(df[cols].mean(axis =1), label = cols, lw = 1.5)
    ax.set(
        ylabel = 'Deriva vertical (m/s)', 
          ylim = [-vmax, vmax], 
          yticks = np.arange(-vmax + 20, vmax + 20, 20),
          )

    ax.axhline(0, linestyle = '--')
    
    # plot_infos(ax, df, site = 'saa')
    
    return None


def plot_QF(ax, df):
    
    ax.bar(df.index, df["QF"],
           width = 0.009, alpha = 0.5)
    
    ax.set(
        ylim = [0, 80], 
        ylabel = "QF (Km)"
        )

    return None


def plot_hF2(ax, df):
    
    ds = df['hmF2'].interpolate()
    ax.plot(ds, lw = 2, color = 'k')
    
    ax.set(
        ylabel = "Altitude (km)", 
        ylim = [100, 600])
    
    return None 



def plot_vz_and_frequencies(dn, cols, site):
    
    file = dn.strftime(f'{site}_%Y%m%d(%j).TXT')
    
    df = dg.IonoChar(file, cols, sel_from = 17)
   
    fig, ax = plt.subplots(
        figsize = (14, 10), 
        nrows = 2, 
        sharex = True, 
        dpi = 300
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    # plot_heights(ax[0], df.heights, cols)
    
    plot_hF2(ax[0], df.chars)
    plot_drift(ax[1], df.drift(), cols, site)
    
    
    # ax[0].legend( 
    #     ncol = 5, 
    #     title = 'Frequências fixas (MHz)',
    #     bbox_to_anchor = (.5, 1.45), 
    #     loc = "upper center", 
    #     columnspacing = 0.3,
    #     fontsize = 30
    #      )
    
    dusk = gg.dusk_from_site(
           dn, 
           site[:3].lower(),
           twilight_angle = 18
           )
    
    ax[0].axvline(
        dusk, lw = 1, linestyle = '--')
    ax[1].axvline(
        dusk, lw = 1, linestyle = '--')
    ax[0].text(
        dusk, 605, 
        'Terminadouro local', 
        transform = ax[0].transData)
    # ax1 = ax[1].twinx()
    # plot_QF(ax1, df.chars )
    b.plot_letters(
        ax, 
        y = 0.85, 
        x = 0.03, 
        fontsize = 40
        )
    
    b.format_time_axes(
        ax[1], 
        pad = 70, 
        translate = False
        )
      
    plt.show()
    
    return fig
    
def main():
    
    cols = list(range(4, 8, 1))
    site = 'SAA0K'
    site = 'FZA0M'
    #dn = dt.datetime(2022, 7, 24)
    dn = dt.datetime(2013, 12, 24)
    dn = dt.datetime(2019, 5, 2)
    
    fig = plot_vz_and_frequencies(dn, cols, site)
    
    FigureName = dn.strftime(f'{site}_%Y%m%d')
       
    # fig.savefig(
    #         b.LATEX(FigureName, folder = 'Iono'),
    #         dpi = 400
    #         )
    
    
# main()