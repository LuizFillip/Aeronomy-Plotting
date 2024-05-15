import GEO as gg
import datetime as dt
import digisonde as dg 
import base as b 
FREQ_PATH = 'digisonde/data/chars/freqs/'

def pipe_data(file):
    df = dg.freq_fixed(FREQ_PATH + file)
    del df[9]
    site, dn = dg.site_datetime_from_file(file, hours = 18)
    
    ds = b.sel_times(df, dn, hours = 12).interpolate()
    
    ds = ds.iloc[1:]
    vz = dg.vertical_drift(ds)
    
    vz = vz.replace(0, float('nan'))
    
    return ds, vz, site



class labels:
    
    def __init__(self, language = 'pt'):
        if language == 'pt':
            self.vz = "Deriva vertical (m/s)"
            self.freq = 'Frequências fixas'
        else:
            self.vz = 'Vertical drift (m/s)'
            self.freq = 'Fixed frequencies'

def plot_terminators(ax, dn, col, shade = False):
         
     dusk = gg.dusk_from_site(
             dn, 
             site = 'saa',
             twilight_angle = 18
             )
     
     delta = dt.timedelta(minutes = 60)
     
     for row in range(2):
         if shade:
              ax[row].axvspan(
                  dusk - delta,
                  dusk + delta,
                  alpha = 0.2, 
                  color = 'gray',
                  lw = 2
              )
                 
         ax[col, row].axvline(
             dusk, 
             linestyle = '-',
             lw = 2,
             color = 'k'
             )
 

     return dusk