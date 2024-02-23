import matplotlib.pyplot as plt 
import base as b
import datetime as dt 
import plotting as pl
from tqdm import tqdm 
import digisonde as dg


def save_img(fig, save_in):
    
    
    fig.savefig(
        save_in, 
        dpi = 300, 
        pad_inches = 0, 
        bbox_inches = "tight"
        )
    
    # FigureName = 'frequencies_and_drift'

    # fig.savefig(
    #     s.LATEX(FigureName, 
    #     folder = 'timeseries')
    #     )
    
    return 


def save_frames(year):
    
   
    infile = 'digisonde/data/jic_freqs.txt'
    df = b.load(infile)

    
    save_in = f'D:\\img3\\{year}\\'
 
    for day in tqdm(range(365), str(year)):
    
        delta = dt.timedelta(days = day)
        
       
        try:
            plt.ioff()
            
            dn = dt.datetime(year, 1, 1, 20) + delta
            
            ds = b.sel_times(
                df, dn, hours = 7).interpolate()
            
            vz = dg.vertical_drift(ds)
            
            fig = pl.plot_vz_and_frequencies(ds, vz, dn)
    
            name = dn.strftime('%j')
    
            save_img(fig, f'{save_in}{name}')
            
            plt.clf()   
            plt.close()
            
        except:
            continue 
        
    return 

for year in [2015, 2019]:
    
    save_frames(year)

