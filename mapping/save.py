import base as b 
import matplotlib.pyplot as plt 
import plotting as pl 
import datetime as dt 
from tqdm import tqdm 
import PlasmaBubbles as pb 
import pandas as pd 


def range_time(start, mi):
        
    return start + dt.timedelta(minutes = mi)


def path_in(start):
    dn_date = start.strftime('%Y%m%d')
    
    return 'database/' + dn_date 
    
    

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
        hours = 9
    else:
        hours = 12
        
    df = b.sel_times(df, start, hours = hours)
    
    save_frames(df, start, hours)
    
# start = dt.datetime(2022, 7, 25, 0)





file = open('dias_tecmap.txt').readlines()

files = [pd.to_datetime(f[15:]) for f in file]


for start in files[2:]:
    # try:
    run(start)

    b.images_to_movie(
            path_in = path_in(start), 
            path_out = 'movies/',
            fps = 12
            )
    # except:
    #     continue 
    