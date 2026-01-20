import core as c 
import base as b 
import matplotlib.pyplot as plt 
import plotting as pl 
from tqdm import tqdm 

path = 'F:\\img\\quiet\\'

df = b.load('core/src/geomag/data/4hours_low_res')

df = c.storms_category(df, col = 'dst_min')

df = c.weak_atypical(df, col = 'kp_max')

ds = df.loc[df['category'] == 'vague']
     
def save_imgs(ds, path_to_save):
    
    '''
    Save os plots com base na categoria de evento
    '''
    
    plt.ioff()

    for dn in tqdm(ds.index):
            
        file = dn.strftime('%Y%m%d.PNG')
        
    # try:
        fig = pl.plot_roti_and_indices(dn)
        fig.savefig(path_to_save + file)
        # except:
        #     print(dn)
        #     continue
        
    plt.clf()   
    plt.close()
    
    return None 
    
    
def main():

    # for cat in df['category'].unique():
    cat = 'quiet'
    
    ds = df.loc[df['category'] == cat]
    
    path_to_save = f'{path}{cat}\\'
    
    b.make_dir(path_to_save)
    
    save_imgs(ds, path_to_save, cat)
        
# main()

path_to_save = 'D:\\img\\vague\\'
save_imgs(ds, path_to_save)


