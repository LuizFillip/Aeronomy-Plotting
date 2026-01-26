import core as c 
import base as b 
import matplotlib.pyplot as plt 
import plotting as pl 
from tqdm import tqdm 


def move_images(dummies):
    import datetime as dt 
    import os 
    import shutil
    
    path_in = 'D:\\img\\vague\\'
    path_out = 'D:\\img\\quiet\\'
    
    dates_out = [
        dt.datetime.strptime(dn, '%Y-%m-%d')
                 for dn in dummies]
    
    for fn in os.listdir(path_in):
        date = dt.datetime.strptime(fn, '%Y%m%d.PNG')
        
        if date not in dates_out:
            
            shutil.move(path_in + fn, path_out + fn)
            
    return None 

     
def save_imgs(ds, path_to_save):
    
    '''
    Save os plots com base na categoria de evento
    '''
    
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
    
    return None 
    
    
def main():
    df = c.category_and_low_indices()
    path_to_save = 'D:\\img\\'
    
    for cat in df['category'].unique():

        ds = df.loc[df['category'] == cat]
        
        path_to_save = f'{path_to_save}{cat}\\'
        
        b.make_dir(path_to_save)
        
        save_imgs(ds, path_to_save)
        
main()




