import GEO as gg 
import datetime as dt  
import matplotlib.pyplot as plt 
import epbs as pb 
import plotting as pl
import base as b  

def get_infos(ds, lon):
    df1 = pb.bubble_features(ds)
    
    infos = df1.loc[
        df1.index == lon, 
        ['type', 'drift']
        ].values.ravel()
    
    Type = infos[0]
    Drift = infos[1]
    
    if Type == Drift:
        return f'{Type}'
    else:
        return f'{Type} - {Drift}'

b.sci_format(fontsize = 25)

def plot_points_and_maximus_roti(
        df, dn, 
        fontsize = 25, 
        translate = True, 
        
        ):

    threshold = 0.30
    
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
    
    vmax = 4
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
                
        l = b.chars()[row]                
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



def main():

    dn = dt.datetime(2022, 12, 4, 21)
    dn = dt.datetime(2022, 6, 13, 21)
    dn = dt.datetime(2015, 4, 13, 21)
    dn = dt.datetime(2023, 12, 11, 21)
    
    df = pb.get_nighttime_roti(dn)
    
    plot_points_and_maximus_roti(df, dn)
    
    plt.show()
        

main()