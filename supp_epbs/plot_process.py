import core as c 
import base as b 
import matplotlib.pyplot as plt 
import plotting as pl 
from tqdm import tqdm 

path = 'E:\\img\\'

df = b.load('core/src/geomag/data/stormsphase')

df = c.geomagnetic_analysis(df)

     
def save_imgs(ds, path_to_save, cat):
    
    plt.ioff()

    for dn in tqdm(ds.index, cat):
            
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

    for cat in df['category'].unique():
    
        ds = df.loc[df['category'] == cat]
        
        path_to_save = f'{path}{cat}\\'
        
        b.make_dir(path_to_save)
        
        save_imgs(ds, path_to_save, cat)
        
main()