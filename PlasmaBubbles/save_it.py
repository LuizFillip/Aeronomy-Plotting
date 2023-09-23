import datetime as dt
import base as b 
import matplotlib.pyplot as plt
from tqdm import tqdm  
import os
from plotting import plot_epbs_occurrences_roti
import PlasmaBubbles as pb 
import pandas as pd


def save_img(ds, func, save_in):

    plt.ioff()
        
    fig = func(ds)
    
    fig.savefig(
        save_in,
        pad_inches = 0, 
        bbox_inches = "tight"
        )
    
    plt.clf()   
    plt.close()
    
    
def save_year(year, root):
    

    b.make_dir(root)
    
    infile = os.path.join(
        pb.PATH_LONG, 
        f'{year}.txt'
        )
    
    out = []
    for day in tqdm(range(365), 
                    desc = str(year)):
        
        delta = dt.timedelta(days = day)
        
        dn = dt.datetime(year, 1, 1, 21) + delta
        
        try:
        
            ds = b.sel_times(
                b.load(infile), 
                dn, hours = 10
                )
            
            out.append(
                pb.get_all_events(ds)
                )
            
            save_in = os.path.join(
                root,  
                dn.strftime('%j.png')
                )
            
            save_img(
                ds, 
                plot_epbs_occurrences_roti, 
                save_in
                )
        except:
            continue
    
    df = pd.concat(out)
    
    save_in = infile.replace('longs', 'events')

    df.to_csv(save_in)
    

        
for year in range(2013, 2021):
    
    root = f'D:\\img\\{year}\\'
    
    save_year(year, root)
    
    
