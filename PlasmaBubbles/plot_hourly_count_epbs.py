import matplotlib.pyplot as plt 
import PlasmaBubbles as pb 
import numpy as np 

def plot(df, title, fontsize = 30):

    fig, ax = plt.subplots(
         figsize = (16, 10),
         nrows = 3,
         ncols = 4,
         sharex = True, 
         sharey = True,
         dpi = 300)
    
    plt.subplots_adjust(hspace = 0.2, wspace = 0.1)
    cols = df.columns
    
    for i, ax in enumerate(ax.flat):
        
        ax.plot(df[cols[i]])
        
        ax.set(ylim = [0, 32],
               title = cols[i],
               xticks = np.arange(20, 36, 4)
               )
        

    fig.text( 
        0.5, 0.05,
        'Hora universal', 
        fontsize = fontsize
        )
    
    name = 'ROTI (TECU/min)'
    name = 'Ocorrências'
    
    fig.text(
        0.05, .32, 
        name , 
        rotation = 'vertical', 
        fontsize = fontsize
        )
    
    fig.suptitle(title)