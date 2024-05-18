import base as b 
import plotting as pl 
import datetime as dt 
import matplotlib.pyplot as plt
import PlasmaBubbles as pb
from tqdm import tqdm 


b.make_dir('temp/')

def save(year = 2019):
    
    for day in tqdm(range(365), str(year)):

        plt.ioff()
        
        delta = dt.timedelta(days = day)
        
        dn = dt.datetime(year, 1, 1, 21) + delta
        
        df = pb.concat_files(
            dn, 
            days = 2, 
            root = 'D:\\', 
            hours = 12
            )
        
        
        # try:
            
        # except:
        #     continue
        fig = pl.plot_points_and_maximus_roti(df, dn)
        name = dn.strftime('D:\\temp\\%Y\\%Y%m%d')    
        fig.savefig(name, dpi = 100)
        
        plt.clf()
        plt.close()

# save(2015)