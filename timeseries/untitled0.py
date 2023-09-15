import base as b 
import pandas as pd 


year = 2013

infile = f"D:\\drift\\{year}.txt"

ds = b.load(infile)

ds

# infile = f'digisonde/data/drift/PRE/saa/{year}.txt'

# ds = b.load(infile)

# ds.rename(columns = {'vp': 'vz'}, 
#       inplace = True)

# infile = 'digisonde/data/PRE/saa/2014_2015_2.txt'


# ds = b.load(infile)

# ds.rename(columns = {'vp': 'vz'}, 
#           inplace = True)


 # ds['vz'].plot(
 #     marker = 'o', 
 #     linestyle = 'none', ylim = [0, 100])

ds.index = pd.to_datetime(ds.index.date)


df = b.load('database/indices/indeces.txt')

df = pd.concat(
    [ds, df], axis = 1).dropna()

df = df.loc[df['kp_max'] < 4]
import matplotlib.pyplot as plt 

x = df['f107'].values
y = df['vz'].values
plt.scatter(x, y)

r2, y_pred = b.linear_fit(x, y)

plt.plot(x, y_pred, label = r2)

plt.legend()


