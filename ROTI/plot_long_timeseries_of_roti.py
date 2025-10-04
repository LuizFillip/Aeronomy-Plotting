import PlasmaBubbles as pb 
import datetime as dt 

dn = dt.datetime(2015, 12, 24, 21)


df = pb.concat_files(
    dn, 
    days = 5, 
    root = 'E:\\', 
    hours = 24 * 3, 
    remove_noise = True
    )

sts = 'ceft'
ds = df.loc[df['sts'] == sts ] 

ds['roti'].plot(ylim = [0, 3]) 