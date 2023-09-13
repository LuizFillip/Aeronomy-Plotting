import base as b 
import datetime as dt

import matplotlib.pyplot as plt
import PlasmaBubbles as pb 

b.config_labels()


df = b.load('roti_evo.txt')

def plot_roti_avg_max():
    

    fig, ax = plt.subplots(
        nrows = 5,
        sharey = True, 
        sharex = True,
        figsize = (10, 10)
        )
    
    
    for i, col in enumerate(df.columns):
        
        ds1 = pb.set_value(df, value = 'mean')
        ax[i].plot(ds1[col])
        
        ds1 = pb.set_value(df, value = 'max')
        ax[i].plot(ds1[col])
