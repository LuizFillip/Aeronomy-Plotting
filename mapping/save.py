import base as b 
import matplotlib.pyplot as plt 
import plotting as pl 
import datetime as dt 
from tqdm import tqdm 
import PlasmaBubbles as pb 
import pandas as pd 
import os 

def range_time(start, mi):
        
    return start + dt.timedelta(minutes = mi)


def path_in(start = None):
    root = 'database/TEC/'
    
   
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
        
        # fig = pl.plot_ipp_variation(df, start, dn )
        
        fig = pl.plot_roti_tec_variation(df, start, dn)
        name = dn.strftime('%Y%m%d%H%M')
                
        fig.savefig(f'{folder}/{name}')
            
        plt.clf()   
        plt.close()    




def run(start, midnight = True):
    
    try:
        df =  pb.concat_files(
            start, 
            root = 'D:\\'
            )
        if midnight:
            hours = 10
        else:
            hours = 12
            
        df = b.sel_times(df, start, hours = hours)
        
        save_frames(df, start, hours)
    
        b.images_to_movie(
                path_in = path_in(start), 
                path_out = 'movies/',
                fps = 12
                )
    except:
        print(start)
        pass


file = open('dias_tecmap.txt').readlines()

files = [pd.to_datetime(f[15:]) for f in file]


folder_created = os.listdir(path_in())

for file in files:
    folder_name = file.strftime('%Y%m%d')
    
    if folder_name not in folder_created:
        run(file, midnight = True)