import base as b 
import matplotlib.pyplot as plt 
import plotting as pl 
import datetime as dt 
from tqdm import tqdm 
import PlasmaBubbles as pb 


def range_time(start, mi):
        
    return start + dt.timedelta(minutes = mi)


def path_in(start = None):
    root = 'database/'
    
   
    if start is None:
        return root
    else:
        return root + start.strftime('%Y%m%d')
    
    

def save_frames(df, start, hours):
    
    '''
    See 'plot_ipp_variation_with_terminator'
    '''
    
    folder =  path_in(start)

    b.make_dir(folder)
    shift = hours * 60 + 1 
    
    for minute in tqdm(range(0, shift), folder):
        
        plt.ioff()
        dn = range_time(start, minute)
        
        fig = pl.plot_ipp_map_and_timeseries(df, start, dn )
        
        # fig = pl.plot_roti_tec_variation(df, start, dn)
        name = dn.strftime('%Y%m%d%H%M')
                
        fig.savefig(f'{folder}/{name}', dpi = 100)
            
        plt.clf()   
        plt.close()    




def run(start):
    
    # try:
    df =  pb.concat_files(
        start, 
        root = 'F:\\'
        )
    if start.hour == 0:
        hours = 10
    else:
        hours = 12
        
    df = b.sel_times(df, start, hours = 12)
    
    save_frames(df, start, hours)

    b.images_to_movie(
            path_in = path_in(start), 
            path_out = 'movies/',
            fps = 5
            )

start = dt.datetime(2014, 1, 2, 21)
# 
# run(start)

b.images_to_movie(
         path_in = path_in(start), 
         path_out = '',
         fps = 10
         )