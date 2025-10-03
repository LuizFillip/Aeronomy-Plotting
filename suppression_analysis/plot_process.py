import core as c 
import os 
import datetime as dt 
import matplotlib.pyplot as plt 
import plotting as pl 


df = c.geomagnetic_analysis()


path = 'E:\\img\\'

# for file in os.listdir(path):
#     fmt = '%Y%m%d.png'
#     dn = dt.datetime.strptime(file, fmt)
#     if dn not in df.index:
#         print(dn)
        
        
        
def save_imgs(ds):
    from tqdm import tqdm 
    
    path = 'E:\\img\\'
    plt.ioff()
    
    for dn in tqdm(ds.index):
        try:
            fig = pl.plot_roti_and_indices(dn)
            fig.savefig(path + dn.strftime('%Y%m%d'))
        except:
            continue
    
    plt.clf()   
    plt.close()
    
    
path = 'E:\\img\\'

import shutil

for dn in df.index:
        
    file = dn.strftime('%Y%m%d.PNG')
    
    cate = df.loc[dn, 'category']
    
    try:
        if cate == 'quiet':
            shutil.move(path + file, f'{path}quiet\\' + file)
        else:
            shutil.move(path + file, f'{path}storm\\' + file)
    except:
        print(dn)
        continue