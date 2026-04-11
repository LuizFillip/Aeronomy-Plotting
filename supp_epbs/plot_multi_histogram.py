import base as b 
import numpy as np 
import core as c 

path = 'drift_pre_test1'
df1 = b.load(path)
df1 = df1.loc[~((df1['vp'] < 0) | 
                (df1['vp'] == 0))]

bins = np.arange(0, 100, 5)



df = c.category_and_low_indices(
        col_kp = 'kp_max', 
        col_dst = 'dst_min'
        )


ds = df1.loc[df1.index.isin(df.index)]

ds['vp'].plot(kind = 'hist', bins = bins) 
