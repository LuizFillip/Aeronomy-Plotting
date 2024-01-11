import base as b 
import matplotlib.pyplot as plt 
import plotting as pl 
import datetime as dt 
from tqdm import tqdm 
import PlasmaBubbles as pb 


def range_time(start, mi):
        
    return start + dt.timedelta(minutes = mi)


def save_maps_with_ipp(df, start):
    
    '''
    See 'plot_ipp_variation_with_terminator'
    '''
    
    folder = start.strftime('D:\\temp\\%Y%m%d')
    b.make_dir(folder)
    
    for minute in tqdm(range(0, 721)):
        
        plt.ioff()
        dn = range_time(start, minute)
        
        # fig = pl.plot_ipp_variation(
        #     df, start, dn
        #     )
        
        fig = pl.plot_roti_tec_variation(df, start, dn)
        name = dn.strftime('%Y%m%d%H%M')
                
        fig.savefig(f'{folder}/{name}')
            
        plt.clf()   
        plt.close()

def main():
    
    start = dt.datetime(2013, 12, 25, 20)
    
    df =  pb.concat_files(
        start, 
        root = 'D:\\'
        )
    
    df = b.sel_times(df, start)
    
    save_maps_with_ipp(df, start)
    
main()