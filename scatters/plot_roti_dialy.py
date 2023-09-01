import GNSS as gs
import base as b 
import matplotlib.pyplot as plt
import numpy as np 


def plot_roti_dialy(df):

    fig, ax = plt.subplots(
        sharex=True, 
        figsize = (10, 8))
        # nrows = 3)
    
    for prn in df.columns:
        
        if 'G' in prn:
            tec = df[prn].dropna()
            
            time_out, rot = gs.rot(
                tec.values, tec.index)
            
    
            # ax[0].plot(tec)
            # ax[1].plot(time_out, rot)
            # ax[0].set(title = f'{prn} - {station}')
            
            t, r = gs.roti(tec.values, tec.index)
            r = np.array(r)
            
            r = np.where(r > 5, np.nan, r)
            ax.scatter(t, r, color = 'b')
            
            ax.set(ylim = [0, 5])
            
    
def sel_prns():
    
    year = 2021

    for doy in range(1, 366, 1):
        
        path = gs.paths(year, doy)
        station = 'ceft'
        
        
        tec = gs.get_tec_from_rinex(
            path, station)
        
        
        ds = gs.run_by_station(
            tec, path, station)
        
        fig, ax = plt.subplots(figsize = (10, 5))
        ds = ds[ds['roti'] < 5]
        
        names = ['GPS', 'GLONASS']
        
        for i, co in enumerate(['G', 'R']):
            
            ds1 = ds[ds['prn'].str.contains(co)]
            ax.scatter(
                ds1.index, ds1['roti'], 
                s = 5,
                label = names[i]
                )
            
            ax.set(ylim = [0, 5], ylabel = 'ROTI', 
                   title = station)
            
            b.format_time_axes(ax, hour_locator = 3)
            
            ax.legend(loc  = 'upper right')
            
            
        save_in = f'D:\\ceft\\{path.doy}.png'
        
        fig.savefig(save_in)