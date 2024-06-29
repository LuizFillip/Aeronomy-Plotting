import matplotlib.pyplot as plt
from skimage import io
import os 

infile = 'C:\\Luiz\\LaTex\\docs\\img\\Ionosphere\\'

file = 'Kelley2009_RegionEDynamo.png'

for file in os.listdir(infile):
        
    fig, ax = plt.subplots(dpi = 400)
    
    save_in = infile + file
    
    ax.imshow(io.imread(save_in))
    
    ax.axis('off')

    fig.savefig(
        save_in, 
        dpi = 700, 
        pad_inches = 0, 
        bbox_inches = "tight", 
        transparent = False
        )