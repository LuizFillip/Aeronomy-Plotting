import base as b 
import plotting as pl 
import datetime as dt 
import matplotlib.pyplot as plt

df = b.load('events_class3')

ds = df.loc[(df['lon'] ==-50) & 
            (df['type'] == 'midnight') & 
            (df['drift'] == 'fresh')]

ds = ds.loc[ds.index > dt.datetime(2017,1,30)]
b.make_dir('temp/')

def save(ds):
    for dn in ds.index:
    
        # dn = dt.datetime(2018, 1, 13, 21)
        # 
        print('', dn)
        plt.ioff()
        
        delta = dt.timedelta(hours = 21)
        ds, df = pl.load_dataset(dn + delta, hours = 14)
        try:
            fig = pl.plot_roti_epb_occurrence_in_column(df, ds)
        except:
            continue
        name = dn.strftime('temp/%Y%m%d')    
        fig.savefig(name)
        
        plt.clf()
        plt.close()
