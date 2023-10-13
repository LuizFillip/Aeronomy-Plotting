import datetime as dt
import base as b 
import matplotlib.pyplot as plt
from tqdm import tqdm  
import os
from plotting import single_plot




    



    

dates = b.random_dates(100)

#%%%

def save_img(dn, func, save_in):

    plt.ioff()
        
    fig = func(dn, 
            cols = [8, 7, 6, 5, 4], 
            hours = 11,
            factor = 5
            )
    
    fig.savefig(
        save_in,
        pad_inches = 0, 
        bbox_inches = "tight"
        )
    
    plt.clf()   
    plt.close()
def run(dates):
    root = 'D:\\img\\factor_5\\'
    
    for dn in tqdm(dates):
        
        save_in = os.path.join(
            root,  
            dn.strftime('%Y%m%d.png')
            )
        
        save_img(
            dn, 
            single_plot, 
            save_in
            )
        
