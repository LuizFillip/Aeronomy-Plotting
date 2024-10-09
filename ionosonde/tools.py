import GEO as gg
import pandas as pd
import numpy as np






class labels:
    
    def __init__(self, language = 'pt'):
        if language == 'pt':
            self.vz = "Deriva vertical (m/s)"
            self.freq = 'Frequências fixas'
        else:
            self.vz = 'Vertical drift (m/s)'
            self.freq = 'Fixed frequencies'

def plot_terminators(ax, df, site):
    
    for dn in np.unique(df.index.date):
        
        dusk = gg.dusk_from_site(
                pd.to_datetime(dn), 
                site = site[:3].lower(),
                twilight_angle = 18
                )
        
        ax.axvline(
            dusk, 
            lw = 2, 
            linestyle = '--', 
            color = 'k'
            )
        
    return None 
