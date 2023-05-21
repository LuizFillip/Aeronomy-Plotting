from setup import *
import os
import cv2

import matplotlib.gridspec as gridspec
import pandas as pd
import locale
from plotTECmaps import *

import cartopy.crs as ccrs




def get_files(infile, extension = ""): 
    _, _, files = next(os.walk(infile))
    
    return [f for f in files if f.endswith(extension)]


def plot_image(img, ax):
    
    if img is not None:
        ax.imshow(img, aspect = "auto")
        
    ax.set(xticks = [], yticks = [])
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.spines.left.set_visible(False)
    ax.spines.bottom.set_visible(False)
    
    return img

def crop_image(file, y = 50, x = 130, h = 900, w = 750):
    img = cv2.imread(file)
    return img[y: y + h, x: x + w]
    






 
def run_for_all_day(date, image_files, tec_files, 
                    iono_files, infile, path_to_save):
    
    out = ordering(date, image_files)

    for num in range(len(out)):
    

        tecFilename, ionoFilename, imagerFilename = tuple(out[num])
    
        
        if imagerFilename == None:
            
            for i in range(10):
                
                plot_quadri_observation(date, 
                                 infile,  
                                 imagerFilename, 
                                 ionoFilename, 
                                 tecFilename, 
                                 save = True, 
                                 path_to_save = path_to_save,
                                 num_time = i)
                
        else:
            
            plot_quadri_observation(date, 
                             infile,  
                             imagerFilename, 
                             ionoFilename, 
                             tecFilename, 
                             save = True, 
                             path_to_save = path_to_save)       
            
            
def layout():
    fig = plt.figure(figsize = (22, 10))
    
    plt.subplots_adjust(wspace = 0.2, hspace = 0.5)
    
    G = gridspec.GridSpec(3, 3)
    
    
    ax1 = plt.subplot(G[0, :])
    ax2 = plt.subplot(G[1:, -1], projection = ccrs.PlateCarree())
    ax3 = plt.subplot(G[1:, 0])

    ax4 = plt.subplot(G[1:, -2])