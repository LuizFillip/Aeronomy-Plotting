import matplotlib.pyplot as plt 
import digisonde as dg
import os 
import shutil 
from tqdm import tqdm 

def  run(dates):

    for dn in tqdm(dates):
            
        maint = 'D:\\ionogram\\'
        
        file = dn.strftime('%Y\\%Y%m%dSA\\')
        
        src = maint + file
        dst = maint + 'quiet\\'
        for fn in os.listdir(src):
                
            if 'RSF'in fn:
              
                shutil.copy(src + fn, dst + fn)
                
infile = 'database/ionogram/20130114S/'

def run():
    import os 
    
    for file in os.listdir(infile):
        if 'PNG' in file:
            dn = dg.ionosonde_fname(file)
            
            plt.ioff()
            
            fig = plot_single_ionogram(
                os.path.join(infile, file), 
                label = True, 
                title = True
                )
            
            FigureName = dn.strftime('%Y%m%d%H%M')
            
            fig.savefig('temp/' + FigureName)
            plt.close()
    
    
    # plt.show()