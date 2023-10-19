import datetime as dt
import base as b 
import matplotlib.pyplot as plt
from tqdm import tqdm  
import os
from plotting import single_plot




    



    

dates = b.random_dates(100)

#%%%

def save_img(dn, func, save_in, factor = 6):

    plt.ioff()
        
    fig = func(dn, 
            cols = [8, 7, 6, 5, 4], 
            hours = 11,
            factor = factor
            )
    
    fig.savefig(
        save_in,
        pad_inches = 0, 
        bbox_inches = "tight"
        )
    
    plt.clf()   
    plt.close()
    
def run(dates, factor = 5):
    
    root = f'D:\\img\\factor_{factor}\\'
    b.make_dir(root)
    
    for dn in tqdm(dates, str(factor)):
        
        save_in = os.path.join(
            root,  
            dn.strftime('%Y%m%d.png')
            )
        
        save_img(
            dn, 
            single_plot, 
            save_in, 
            factor
            )
        
# run(dates)
factor = 4
root = f'D:\\img\\factor_{factor}\\'

files = os.listdir(root)
import os 
for dn in dates:
    fn = dn.strftime('%Y%m%d.png')
    fname = os.path.join(
        root,  
        fn
        )
    
    if fn in files:
        print(dn)
    # else:
    #     os.remove(fname)