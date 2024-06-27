import GEO as gg 
import datetime as dt  
import matplotlib.pyplot as plt 
import PlasmaBubbles as pb 
import plotting as pl
import base as b  

b.config_labels(fontsize = 30)

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


def plot_points_and_maximus_roti(
        df, dn, 
        fontsize = 30, 
        vmax = 4, 
        translate = True
        ):
    
    threshold  = pb.threshold(dn, factor = 4)['noise'].item()
    threshold = round(threshold, 3)
    
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
        figsize = (16, 12)
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
                
        l = b.chars()[row]                
        info = f'({l}) {sector_name} {row + 1} ({sector}°)'
        
        ax[row].text(
            0.01, 0.8, info, 
            transform = ax[row].transAxes
            )
        
        if row == 0:
            label_top = vmax + 2.2
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
            ylim = [0, vmax + 2], 
            yticks = list(range(0, 6, 1)), 
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
            fontsize = 25, 
            s = 80, 
            threshold = threshold,
            anchor = (0.5, 4.8), 
            ncol = 3
            )
    return fig 



def main():
  
    dates = [dt.datetime(2015, 12, 20, 21), 
             dt.datetime(2017, 9, 17, 21),
             dt.datetime(2013, 1, 17, 21),
             dt.datetime(2014, 2, 9, 21)]
    
    dn = dates[3]
    # dn = dt.datetime(2013, 1, 26, 21)
    # dn = dt.datetime(2014, 4, 28, 21)
    df = pb.concat_files(
        dn, 
        days = 2, 
        root = 'E:\\', 
        hours = 12, 
        remove_noise = True
        )
    
    
    fig = plot_points_and_maximus_roti(
            df, 
            dn, 
            fontsize = 30, 
            translate = False
            )
    
    FigureName = dn.strftime('occurrence_%Y%m%d')
    
    
    fig.savefig(
          b.LATEX(FigureName, folder = 'timeseries'),
          dpi = 400
          )
    

    plt.show()
        

# main()