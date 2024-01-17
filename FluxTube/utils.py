import pandas as pd 


def load_fluxtube(dn = '2013-12-24 22:00:00'):
    
    infile = "20131224sep.txt"
    
    df = pd.read_csv(infile, index_col = 0)
    
    return df.loc[df['dn'] == dn]
