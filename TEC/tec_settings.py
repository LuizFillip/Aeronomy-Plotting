import pandas as pd
import numpy as np

def load_tec(infile, values = True):

    df = pd.read_csv(
        infile, 
        delimiter = ';', 
        header = None
        ).replace(-1, np.nan)
    
    xmax, ymax = df.values.shape
   
    df.columns = np.arange(0, ymax)*0.5 - 90
    df.index = np.arange(0, xmax)*0.5 - 60
    
    if values:
        return df.columns, df.index, df.values
    else:
        return df

# load_tec(infile, values = True)