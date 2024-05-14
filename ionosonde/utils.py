import GEO as gg
import datetime as dt

class labels:
    
    def __init__(self, language = 'pt'):
        if language == 'pt':
            self.vz = "Deriva vertical (m/s)"
            self.freq = 'Frequências fixas'
        else:
            self.vz = 'Vertical drift (m/s)'
            self.freq = 'Fixed frequencies'

def plot_terminators(ax, dn, shade = False):
         
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
                 
         ax[row].axvline(
             dusk, 
             linestyle = '-',
             lw = 2,
             color = 'k'
             )
 

     return dusk