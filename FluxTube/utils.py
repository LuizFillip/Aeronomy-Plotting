import pandas as pd 



dn = '2013-12-24 22:00:00'


def load_sep(dn = dn):
    
    infile = "20131224sep.txt"
    
    df = pd.read_csv(infile, index_col = 0)
    
    return df.loc[df['dn'] == dn]


