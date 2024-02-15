import matplotlib.pyplot as plt 
import base as b 
import PlasmaBubbles as pb 
import datetime as dt
import GEO as gg 
import os 



def load_data():
    
    dn = dt.datetime(2013, 12, 24, 20)
        
    
    df = pb.concat_files(
            dn, 
            root = 'D:\\' ,
            days = 1
            )

    
    df = df.loc[df['el'] > 30]
    
    coords = gg.set_coords(dn.year, radius = 10)
    
    sector = -60
    
    ds = pb.filter_coords(df, sector, coords)
    
    ds['roti'].plot(ylim = [0, 3])
    



# load_data()

# dn = dt.datetime(2013, 12, 24, 20)
    

# df = pb.concat_files(
#         dn, 
#         root = 'D:\\' ,
#         days = 1
#         )


# df