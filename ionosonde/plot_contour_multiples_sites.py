import matplotlib.pyplot as plt
import base as b 
import digisonde as dg 
import numpy as np 
import datetime as dt 
import GEO as gg 

b.config_labels()




def plot_QF(ax, df, color):
    
    ax.bar(
        df.index, 
        df["QF"],
        width = 0.01, 
        color = color,
        alpha = 0.7,
        )
    
    ax.set(ylim = [0, 60])
    
    return None 


def plot_terminator(ax, dn, site):
    
    dusk = gg.dusk_from_site(
           dn, 
           site,
           twilight_angle = 18
           )
        
    ax.axvline(
        dusk, lw = 2, linestyle = '--')
    
    start = dt.datetime(2015, 12, 21, 6, 30)
    ax.axvspan(
         start, 
         start + dt.timedelta(hours = 1), 
         ymin = 0, 
         ymax = 1,
         alpha = 0.2, 
         color = 'gray'
         )
    
    return dusk

def plot_multiples_sites(
        ref,
        cols, 
        dn,
        fontsize = 40
        ):
    
   
    fig, ax = plt.subplots(
         figsize = (20, 12), 
         ncols = 2, 
         nrows = 2,
         sharex = True, 
         dpi = 300
         )

    plt.subplots_adjust(
        hspace = 0.05, 
        wspace = 0.3
        )

    cols = list(range(4, 8, 1))

    codes = ['SAA0K', 'BVJ03']# 'JI91J']
    sites = ['saa', 'bvj'] #'jic']
    for i, site in enumerate(codes):
    
        df = dg.IonoAverage(dn, cols, site, ref = ref)
              
        plot_heights(ax[i, 0], df, parameter)
        
        plot_drift(ax[i, 1], df, vmax = 50)
       

        s = f'{df.data.site}'
        
        x = 0.03
        y = 0.84
        ax[i, 0].text(
            x, y, s, 
            transform = ax[i, 0].transAxes
            )
        ax[i, 1].text(
            x, y, f'{df.data.site}', 
            transform = ax[i, 1].transAxes
            )
        
    
        dusk = plot_terminator(ax[i, 0],  ref,sites[i])
        dusk = plot_terminator(ax[i, 1],  ref,sites[i])
        
        if i == 0:
            ax[0, 0].text(
                dusk, 605, 
                'Terminadouro local', 
                transform = ax[0, 0].transData
                )
            
            ax[0, 1].text(
                dusk, 55, 
                'Terminadouro local', 
                transform = ax[0, 1].transData
                )
             
    end = ref + dt.timedelta(hours = 14)

    ax[-1, 0].set(xlim = [ref, end])
        
    b.format_time_axes(ax[-1, 0], pad = 80, hour_locator = 2)
    b.format_time_axes(ax[-1, 1], pad = 80, hour_locator = 2)

    ax[0, 0].legend(
          ncol = 6, 
          loc = "upper right", 
          bbox_to_anchor = (1.7, 1.4), 
          )
    
    ax[0, 0].text(
        -0.1, 1.1, '(a)',
        fontsize = fontsize,
        transform = ax[0, 0].transAxes
        )
    ax[0, 1].text(
        -0.1, 1.1, '(b)',
        fontsize = fontsize,
        transform = ax[0, 1].transAxes
        )
    fig.text(
        0.04, 0.4,
        'Altura (km)', 
        rotation = 'vertical',
        fontsize = fontsize
        )
    fig.text(
        0.48, 0.3,
        'Deriva vertical (m/s)', 
        rotation = 'vertical',
        fontsize = fontsize
        )
    

    return fig



def plot_drift(ax, df, vmax = 60):
    
    vz = df.ref_data.drift() 
    qt = df.drift
    ax.plot(vz['vz'], lw = 1.5, label = 'Perturbado')
    
    ax.plot(qt['vz'], lw = 1.5, label = 'Calmo')
    ax.axhline(0, linestyle = '--')
     
    ax.set(
        ylim = [-vmax + 10, vmax], 
        yticks = np.arange(-vmax + 10, vmax + 10, 20)
        )
    
    return None
    

def plot_heights(ax, df, parameter = 'hmF2'):
    
    hf = df.ref_data.chars

    qt = df.chars(parameter)

    ax.plot(hf[parameter], lw = 1.5, label = 'Perturbado')

    ax.plot(qt[parameter], lw = 1.5, label = 'Calmo')
    
    ax.set(ylim = [100, 600])
    
    return None

 
ref = dt.datetime(2015, 12, 20, 20)

dn = dt.datetime(2015, 12, 2)


def main():
    cols = list(range(4, 8, 1))
    
    fig = plot_multiples_sites(ref, cols,  dn)
    
    FigureName = ref.strftime('Iono_parameters_%Y%m%d')
    
    # fig.savefig(
    #       b.LATEX(FigureName, folder = 'Iono'),
    #       dpi = 400
    #       )
    
    # plt.show()
