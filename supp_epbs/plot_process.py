import core as c 
import base as b 
import matplotlib.pyplot as plt 
import plotting as pl 
from tqdm import tqdm 


     
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




