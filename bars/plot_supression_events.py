import core as c
import base as b 
import matplotlib.plot as plt 
lon = -50

df = atypical_frame(lon, kind = 0, days = 3)

ds = c.count_occurences(df).month

fig, ax = plt.subplots()

ds['epb'].plot(kind = 'bar')
