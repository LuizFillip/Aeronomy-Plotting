import pandas as pd 



dn = '2013-12-24 22:00:00'


def load_fluxtube(dn = dn):
    
    infile = "plotting/FluxTube/data/20131224sep.txt"
    
    df = pd.read_csv(infile, index_col = 0)
    
    return df.loc[df['dn'] == dn]


def total(out):
    return pd.concat(out, axis = 1).sum(axis = 1)

# infile = 'total_20131224'
# df = pd.read_csv(infile, index_col = 0)

# df