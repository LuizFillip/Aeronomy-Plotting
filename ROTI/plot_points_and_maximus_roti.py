import GEO as gg 
import datetime as dt  
import matplotlib.pyplot as plt 
import epbs as pb 
import plotting as pl
import base as b  
import pandas as pd
from pathlib import Path 
 
def get_infos(ds, lon):
    df1 = pb.bubble_features(ds)
    
    infos = df1.loc[ df1.index == lon,  
                    ['type', 'drift'] ].values.ravel()
    
    Type = infos[0]
    Drift = infos[1]
    
    if Type == Drift:
        return f'{Type}'
    else:
        return f'{Type} - {Drift}'

b.sci_format(fontsize = 25)

def plot_points_and_maximus_roti(
        df, 
        dn, 
        fontsize = 25, 
        threshold = 0.30,
        translate = True, 
        vmax = 4
        ):

    
    
    if translate:
        occurrence = 'Occurrence'
        sector_name = 'Sector'
    else:
        occurrence = 'Ocorrência'
        sector_name = 'Setor'
        
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 4,
        sharex = True,
        sharey = True,
        figsize = (12, 10)
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    coords = gg.set_coords(dn.year)
    
    
    for row, sector in enumerate(coords.keys()):
        
        if sector != -80:
            df1 = pb.removing_noise(df)
        else:
            df = df.copy()
            
        ds = pb.filter_region(df1, dn.year, sector)

        ds = pl.plot_roti_points(
                ax[row], ds, 
                threshold = threshold,
                label = False, 
                points_max = True, 
                )
                
        l = b.letters()[row]                
        info = f'({l}) {sector_name} {row + 1}'
        
        ax[row].text(
            0.01, 0.8, info, 
            transform = ax[row].transAxes
            )
        
        if row == 0:
            label_top = vmax + 0.3
        else:
            label_top = None
        
        pl.plot_references_lines(
                ax[row],
                sector, 
                dn, 
                label_top = label_top,
                translate = translate
                )
        
        ax[row].set(
            ylim = [0, vmax + 0.2], 
            yticks = list(range(0, 4, 1)), 
            xlim = [df.index[0], df.index[-1]], 
            )
        
        
    b.format_time_axes(ax[-1], translate = translate)
    
    
    fig.text(
        0.05, 0.35, 
        'ROTI (TECU/min)', 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.93, 0.42, 
        occurrence, 
        fontsize = fontsize, 
        rotation = 'vertical', 
        color = 'b'
        ) 
    
    pl.legend_max_points_roti(
            ax[0], 
            fontsize = fontsize, 
            s = 80, 
            threshold = threshold,
            translate = translate,
            anchor = (0.5, 4.8), 
            ncol = 3
            )
    return fig 



  
def save_figures(dates):
   
    plt.ioff()
    for dn in dates:
        
        delta = dt.timedelta(hours = 21)
        dn = pd.Timestamp(dn)  + delta
        
        fn = dn.strftime('%Y%m%d')
       
        path_to_save =  Path('D:\\img\\dummies\\') / fn 
        
        if not path_to_save.exists():
       
            df = pb.get_nighttime_roti(dn, root = 'D:\\')
            
            fig = plot_points_and_maximus_roti(df, dn)
        
            print('saving', fn)
            fig.savefig(path_to_save)
        
    plt.clf()   
    plt.close()
    
# main()

# from SuppressionEPBs import load_suppressions

# df = load_suppressions(days = 2)
# dates = df.index

# save_figures(dates)
delta = dt.timedelta(hours = 21)
dn = pd.Timestamp('2022-04-12')  +  delta
df = pb.get_nighttime_roti(dn, root = 'D:\\')

fig = plot_points_and_maximus_roti(df, dn)

 
# plt.show()

df