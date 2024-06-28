# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 16:43:49 2024

@author: Luiz
"""

import os 
from skimage import io
import matplotlib.pyplot as plt 

infile = 'C:\\Luiz\\LaTex\\docs\\img\\maps\\map_sequence.png'




fig, ax = plt.subplots(
    dpi = 300
    )


ax.imshow(io.imread(infile))

ax.axis('off')

fig.savefig(infile, dpi = 1000)