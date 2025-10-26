import core as c 
import base as b
import datetime as dt 
import matplotlib.pyplot as plt 
import plotting as pl 
from tqdm import tqdm 

path = 'E:\\img\\'

# for file in os.listdir(path):
#     fmt = '%Y%m%d.png'
#     dn = dt.datetime.strptime(file, fmt)
#     if dn not in df.index:
#         print(dn)

df = b.load('core/src/geomag/data/stormsphase')


# fig = plot_roti_and_indices(dn)

df = c.geomagnetic_analysis(df)

        
path = 'E:\\img\\'

     
def save_imgs(ds, path_to_save):
    
    plt.ioff()

    for dn in tqdm(ds.index):
            
        file = dn.strftime('%Y%m%d.PNG')
        
        try:
            fig = pl.plot_roti_and_indices(dn)
            fig.savefig(path_to_save + file)
        except:
            print(dn)
            continue
        
    plt.clf()   
    plt.close()
    
    
def main():

    # for cat in df['category'].unique():
    
    cat = 'intense'
        
    ds = df.loc[df['category'] == cat]
    
    path_to_save = f'{path}{cat}\\'
    
    b.make_dir(path_to_save)
    
    save_imgs(ds, path_to_save)
        