import base as b 
import matplotlib.pyplot as plt 
import plotting as pl 
import datetime as dt 


def range_time(start, mi):
        
    return start + dt.timedelta(minutes = mi)

def save_maps_with_ipp(df, start):
    
    '''
    See 'plot_ipp_variation_with_terminator'
    '''
    
    folder = start.strftime('%Y%m%d')
    b.make_dir(folder)
    
    for minute in range(0, 721):
        
        plt.ioff()
        dn = range_time(start, minute)
        
        fig = pl.plot_ipp_variation(
            df, start, dn
            )
        name = dn.strftime('%Y%m%d%H%M')
        
        print(minute, name)
        
        fig.savefig(f'{folder}/{name}')
            
        plt.clf()   
        plt.close()
        