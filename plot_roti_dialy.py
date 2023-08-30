import GNSS as gs

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