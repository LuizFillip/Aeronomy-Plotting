import matplotlib.pyplot as plt
import base as b 
import digisonde as dg 
import numpy as np 
import datetime as dt 

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

   
def plot_multiples_sites(
        ref,
        cols, 
        dn,
        fontsize = 30
        ):
    
   
    fig, ax = plt.subplots(
         figsize = (16, 12), 
         ncols = 2, 
         nrows = 3,
         sharex = True, 
         dpi = 300
         )

    plt.subplots_adjust(
        hspace = 0.05, 
        wspace = 0.3
        )

    cols = list(range(4, 8, 1))

    codes = ['SAA0K', 'BVJ03', 'JI91J']

    for i, site in enumerate(codes):
        
      
        df = dg.IonoAverage(dn, cols, site, ref = ref)
        
        if site == 'JI91J':
            parameter = 'hF'
        else:
            parameter = 'hF2'
            
        plot_heights(ax[i, 0], df, parameter)
        
        plot_drift(ax[i, 1], df, vmax = 50)
       

        s = f'({b.chars()[i]}) {df.data.site}'
        
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
        
    end = ref + dt.timedelta(hours = 14)

    ax[-1, 0].set(xlim = [ref, end])
        
    b.format_time_axes(ax[-1, 0], hour_locator = 2)
    b.format_time_axes(ax[-1, 1], hour_locator = 2)

    ax[0, 0].legend(
          ncol = 6, 
          loc = "upper right", 
          bbox_to_anchor = (1.5, 1.43), 
          )
    
    ax[1, 0].set_ylabel(
        'h`F (km)', 
        fontsize = fontsize
        )
    ax[1, 1].set_ylabel(
        'Vertical drift (m/s)', 
        fontsize = fontsize
        )
    

    return fig



def plot_drift(ax, df, vmax = 60):
    
    vz = df.ref_data.drift() 
    qt = df.drift
    # print(qt)
    ax.plot(vz['vz'], lw = 1.5, label = 'Disturbed')
    
    ax.plot(qt['vz'], lw = 1.5, label = 'Quiet')
    
    # ax.fill_between(qt.index, 
    #                 qt['vz'] +  qt['dvz'], 
    #                 qt['vz'] -  qt['dvz'], 
    #                 alpha = 0.3)
    
    ax.axhline(0, linestyle = '--')
     
    ax.set(
        ylim = [-vmax + 10, vmax], 
        yticks = np.arange(-vmax + 10, vmax + 10, 20)
        )
    
    return None
    

def plot_heights(ax, df, parameter = 'hmF2'):
    
    hf = df.ref_data.chars

    qt = df.chars(parameter)

    ax.plot(hf[parameter], lw = 1.5, label = 'Disturbed')

    ax.plot(qt[parameter], lw = 1.5, label = 'Quiet')
    
    ax.set(ylim = [100, 600])
    
    return None

 
ref = dt.datetime(2015, 12, 20, 20)

dn = dt.datetime(2015, 12, 2)


dn = dt.datetime(2013, 3, 4, 20)

ref = dt.datetime(2013, 3, 17)


cols = list(range(4, 8, 1))


# fig = plot_multiples_sites(ref, cols,  dn)


# FigureName = ref.strftime('Iono_parameters_%Y%m%d')
# # fig.savefig(
# #       b.LATEX(FigureName, folder = 'paper2'),
# #       dpi = 400
# #       )

# plt.show()

import GEO as gg 


def plot_compare_quiet_disturbed(ref_lon = -50):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        figsize = (12, 8), 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    site = 'SAA0K'
    
    df = dg.IonoAverage(dn, cols, site, ref = ref)
            
    plot_heights(ax[0], df, parameter = 'hF2')
    
    plot_drift(ax[1], df, vmax = 50)
    
    start = dt.datetime(2013, 3, 17, 20)
    end = dt.datetime(2013, 3, 18, 10)
    
    
    ax[0].set(
        xlim = [start, end],
        ylabel = 'h`F (km)'
        )
    ax[1].set_ylabel(
        'Vertical drift (m/s)'
        )
    
    
    
    ax[0].legend(loc = 'upper center', ncols = 2)
    
    
    
    dusk = gg.terminator(
        -50, 
        ref, 
        float_fmt = False
        )
    
    ax[0].axvline(dusk)
    ax[1].axvline(dusk)
        
    b.format_time_axes(ax[-1], translate = True)
    
    
plot_compare_quiet_disturbed()