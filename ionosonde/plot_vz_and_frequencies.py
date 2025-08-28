import matplotlib.pyplot as plt
import digisonde as dg
import base as b 
import GEO as gg 
import datetime as dt 
import numpy as np

b.sci_format(fontsize = 30)


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

def plot_drift(
        ax, df, cols, 
        site, vmax = 60, 
        translate = False):
    
    if translate:
        ylabel = 'Vertical drift (m/s)'
        
    else:
        ylabel = 'Velocidade de \nderiva vertical (m/s)'
        
    ax.plot(
        df[cols],
        label = cols, lw = 1.5)
    
    ax.set(
        ylabel = ylabel, 
        ylim = [-vmax, vmax], 
        yticks = np.arange(-vmax + 20, vmax + 20, 20),
        )

    ax.axhline(0, linestyle = '--')
    
    plot_infos(ax, df, site = 'saa')
    
    return None


def plot_QF(ax, df):
    
    ax.bar(
        df.index, 
        df["QF"],
        width = 0.009, 
        alpha = 0.5
        )
    
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



def plot_vz_and_frequencies(
        dn, 
        cols, 
        site, 
        sum_from = 17, 
        translate = False
        ):
    
    if translate:
        term_name = 'Local terminator'
        title = 'Fixed Frequencies'
        
       
    else:
        term_name = 'Terminadouro local'
        title = 'Frequências fixas (MHz)'
        
    
    file = dg.dn2fn(dn, site)
    
    df = dg.IonoChar(file, cols, sum_from = sum_from)
   
    fig, ax = plt.subplots(
        figsize = (14, 10), 
        nrows = 2, 
        sharex = True, 
        dpi = 300
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    plot_heights(ax[0], df.heights, cols)
    
    # plot_hF2(ax[0], df.chars)
    plot_drift(ax[1], df.drift(), cols, site, 
               translate = translate)
    
    
    ax[0].legend( 
        ncol = 5, 
        title = title,
        bbox_to_anchor = (.5, 1.45), 
        loc = "upper center", 
        columnspacing = 0.3,
        fontsize = 30
          )
    
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
        dusk, 500, term_name, 
        transform = ax[0].transData)
    ax1 = ax[1].twinx()
    plot_QF(ax1, df.chars )
    b.plot_letters(
        ax, 
        y = 0.85, 
        x = 0.03, 
        fontsize = 40
        )
    
    b.format_time_axes(
        ax[1], 
        pad = 70, 
        translate = translate
        )
      
    plt.show()
    
    return fig
    
def main():
    
    cols = list(range(3, 8, 1))
    site = 'SAA0K'
    # site = 'FZA0M'
    dn = dt.datetime(2022, 7, 25, 0)
    dn = dt.datetime(2013, 12, 24, 16)
    # dn = dt.datetime(2019, 5, 2)
    # dn = dt.datetime(2016, 10, 3)

    fig = plot_vz_and_frequencies(dn, cols, site, translate= True)
    
    FigureName = dn.strftime(f'{site}_%Y%m%d')
       
    # fig.savefig(
    #         b.LATEX(FigureName, folder = 'posdoc'),
    #         dpi = 400
    #         )
    
    
# main()
