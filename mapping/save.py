import base as b 
import matplotlib.pyplot as plt 
import plotting as pl 
import datetime as dt 
from tqdm import tqdm 
import PlasmaBubbles as pb 


def range_time(start, mi):
        
    return start + dt.timedelta(minutes = mi)


def save_frames(df, start, hours):
    
    '''
    See 'plot_ipp_variation_with_terminator'
    '''
    dn_date = start.strftime('%Y%m%d')
    
    folder = 'database/' + dn_date 
    
    b.make_dir(folder)
    shift = hours * 60 + 1 
    for minute in tqdm(range(0, shift), dn_date):
        
        plt.ioff()
        dn = range_time(start, minute)
        
        # fig = pl.plot_ipp_variation(df, start, dn )
        
        fig = pl.plot_roti_tec_variation(df, start, dn)
        name = dn.strftime('%Y%m%d%H%M')
                
        fig.savefig(f'{folder}/{name}')
            
        plt.clf()   
        plt.close()

def run(start, midnight = True):
    
    
    df =  pb.concat_files(
        start, 
        root = 'D:\\'
        )
    if midnight:
        hours = 8
    else:
        hours = 12
        
    df = b.sel_times(df, start, hours = hours)
    
    save_frames(df, start, hours)
    
start = dt.datetime(2022, 7, 25, 0)

run(start)