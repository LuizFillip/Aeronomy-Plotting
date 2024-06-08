import GEO as gg
import datetime as dt
import digisonde as dg 
import base as b 





class labels:
    
    def __init__(self, language = 'pt'):
        if language == 'pt':
            self.vz = "Deriva vertical (m/s)"
            self.freq = 'Frequências fixas'
        else:
            self.vz = 'Vertical drift (m/s)'
            self.freq = 'Fixed frequencies'

def plot_terminators(ax, dn, col = None, shade = False):
         
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
         
         if col is None:
                    
             ax[row].axvline(
                 dusk, 
                 linestyle = '-',
                 lw = 2,
                 color = 'k'
                 )
            
         else:
             ax[row, col].axvline(
                 dusk, 
                 linestyle = '-',
                 lw = 2,
                 color = 'k'
                 )

     return dusk
 
# file = 'SAA0K_20130516(136).TXT'

# df = dg.freq_fixed(FREQ_PATH + file)
# ds = df.iloc[1:].interpolate()
# vz = dg.vertical_drift(ds)

# vz 