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
        fontsize = 35, 
        vmax = 4, 
        translate = True
        ):
    
    threshold  = pb.threshold(dn, factor = 4)['noise'].item()
    threshold = round(threshold, 3)
    threshold = 0.2
    
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
        figsize = (16, 12)
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
        
        # if sector <= - 70:
        #     ds = ds.loc[~(ds['roti']> 0.25)]
            
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
            fontsize = 32, 
            s = 80, 
            threshold = threshold,
            translate = translate,
            anchor = (0.5, 4.8), 
            ncol = 3
            )
    return fig 



def main():
  
    dates = [dt.datetime(2015, 12, 20, 21), 
             dt.datetime(2017, 9, 17, 21),
             dt.datetime(2013, 1, 17, 21),
             dt.datetime(2014, 2, 9, 21)]
    
    dn = dates[2]
    dn = dt.datetime(2019, 12, 6, 21)
    dn = dt.datetime(2018, 12, 12, 21)
    dn = dt.datetime(2018, 6, 11, 21)
    dn = dt.datetime(2019, 12, 20, 21)
    dn = dt.datetime(2013, 1, 17, 21)
    
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
            fontsize = 35, 
            translate = True
            )
    
    FigureName = dn.strftime('%Y%m%d')
    
    
    # fig.savefig(
    #       b.LATEX(FigureName, folder = 'ROTI'),
    #       dpi = 400
    #       )
    
    save_in = 'G:\\My Drive\\Papers\\Paper 2\\Midnight EPBs\\Eps\\img\\'

    fig.savefig(save_in + FigureName, dpi = 300
                )
    
    

    plt.show()
        

# main()