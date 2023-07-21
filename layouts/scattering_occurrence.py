import numpy as np
import matplotlib.dates as dates
import matplotlib.pyplot as plt
import os
from utils import datetime_from_fn
root = "D:\\FluxTube\\"

res = {}
for folder in os.listdir(root):
    infile = os.path.join(root, folder)
    month = {folder : []}
    res.update(month)
    for filename in os.listdir(infile):
        month[folder].append(datetime_from_fn(filename))
   
     
#%%
fig, ax = plt.subplots(figsize = (12, 3))

for key in res.keys():

    days = np.unique([x.day for x in res[key]])
    times = []
    for day in days:
        times.append(np.sum([(t.hour + (t.minute/60)) /20 for t in res[key] if t.day == day]))
    month = np.zeros(len(days)) + int(key)
    img = ax.scatter(days, month, c = times)

plt.colorbar(img)

ax.set(ylim = [0, 12], yticks = np.arange(1, 13, 1), 
       xticks = np.arange(1, 31, 1))

#%%

days = np.unique([x.day for x in res[key]])

                         
len(times), len(days)

    