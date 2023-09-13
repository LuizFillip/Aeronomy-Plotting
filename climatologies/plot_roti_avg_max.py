import base as b 
import datetime as dt

import matplotlib.pyplot as plt
import PlasmaBubbles as pb 

b.config_labels()


df = b.load('roti_evo.txt')

fig, ax = plt.subplots(
    figsize = (10, 5), 
    dpi = 300
    )

ax.plot(df)

ax.legend(['average', 
           'maximum'])

ax.set(ylabel = 'ROTI (TECU/min)', 
       xlabel = 'Years')