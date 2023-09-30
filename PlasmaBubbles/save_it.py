import datetime as dt
import base as b 
import matplotlib.pyplot as plt
from tqdm import tqdm  
import os
from plotting import single_plot



def save_img(dn, func, save_in):

    plt.ioff()
        
    fig = func(dn)
    
    fig.savefig(
        save_in,
        pad_inches = 0, 
        bbox_inches = "tight"
        )
    
    plt.clf()   
    plt.close()
    
    
def save_year(year, root):
    

    b.make_dir(root)
    
    for day in tqdm(range(365), 
                    str(year)):
        
        delta = dt.timedelta(days = day)
        
        dn = dt.datetime(year, 1, 1, 21) + delta
                
        save_in = os.path.join(
            root,  
            dn.strftime('%j.png')
            )
        
        save_img(
            dn, 
            single_plot, 
            save_in
            )
    
    

        
for year in range(2013, 2023):
    root = f'D:\\img\\{year}\\'
    
    save_year(year, root)
    
    
