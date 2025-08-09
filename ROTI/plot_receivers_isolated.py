import GEO as gg 
import datetime as dt  
import matplotlib.pyplot as plt 
import PlasmaBubbles as pb 
import plotting as pl
import base as b  

dn = dt.datetime(2015, 12, 20, 20)


df = pb.concat_files(
    dn, 
    days = 2, 
    root = 'E:\\', 
    hours = 12, 
    remove_noise = True
    )

station = 'paat' #, 'ceeu' #'pbjp' #'ceft' #'rnna'

ds = df.loc[df['sts'] == station]

ds['roti'].plot(ylim = [0, 2])