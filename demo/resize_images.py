import os 
from skimage import io
import matplotlib.pyplot as plt 

infile = 'C:\\Luiz\\LaTex\\docs\\img\\modeling\\fluxogram.png'




fig, ax = plt.subplots(
    dpi = 300
    )


ax.imshow(io.imread(infile))

ax.axis('off')

fig.savefig(infile, dpi = 1500, 
pad_inches = 0, 
bbox_inches = "tight", 
transparent = False)