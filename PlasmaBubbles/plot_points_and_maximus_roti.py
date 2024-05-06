import GEO as gg 
import datetime as dt  
import matplotlib.pyplot as plt 
import PlasmaBubbles as pb 
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


def plot_points_and_maximus_roti(
        df, dn, 
        threshold = 0.25,
        fontsize = 30
        ):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 4,
        sharex = True,
        figsize = (10, 12)
        )
    
    plt.subplots_adjust(hspace = 0.3, wspace = 0.03)
    
    coords = gg.set_coords(dn.year)
    
    out_infos = []
    for row, sector in enumerate(coords.keys()):
    
        ds = pb.filter_coords(df, sector, coords)
        
        ds = pl.plot_roti_points(
                ax[row], ds, 
                threshold = threshold,
                label = False, 
                points_max = True
                )
                
        terminator = gg.terminator(
            sector, dn, float_fmt = False)
        
        ax[row].axvline(terminator, color = 'k', lw = 2)
                        
        info = f'Sector {row + 1} ({sector}°)'
        
        ax[row].text(
            0.01, 1.05, info, 
            transform = ax[row].transAxes
            )
        
        delta = dt.timedelta(hours = 3)
        midnight = gg.local_midnight(dn + delta, sector)
        
        ax[row].axvline(
            midnight, color = 'k', lw = 2, linestyle = '--')
        ax[row].set(
            ylim = [0, 3], 
            xlim = [df.index[0], df.index[-1]],
            title = get_infos(ds, lon = int(sector))
            )
        
        if row == 0:
            out_infos.extend([terminator, midnight])
      
    b.format_time_axes(ax[-1], translate = False)
    
    
    fig.text(0.03, 0.33, 'ROTI (TECU/min)', 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(0.93, 0.42, 'Occurrence', 
        fontsize = fontsize, 
        rotation = 'vertical'
        ) 
    
    return fig 



def main():
  
    dn = dt.datetime(2014, 5, 1, 21)
    
    
    df = pb.concat_files(
        dn, 
        days = 2, 
        root = 'D:\\',#os.getcwd(),
        hours = 12
        )
    
    
    fig = plot_points_and_maximus_roti(
            df, 
            dn, 
            threshold = 0.25,
            fontsize = 30
            )
    
    
    plt.show()
    
    
    
# main()
