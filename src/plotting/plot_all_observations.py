from setup import *
import os
import cv2

import matplotlib.gridspec as gridspec
import pandas as pd
import locale


from GNSS.plotConfig import mapping
from plotTECmaps import *

import cartopy.crs as ccrs

from imager.image_settings import load_and_processing
from imager.image_labeling import draw_labels

from results.results_utils import ordering, date_from_filename

from results.plot.plotROTImaximus import *


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
    




def plot_quadri_observation(date, 
                            infile,
                            imagerFilename, 
                            ionoFilename, 
                            tecFilename, 
                            save = False, 
                            path_to_save = "C:\\tri_observation", 
                            num_time = 0):
    
    if save:
        plt.ioff()
        
        
    delta = datetime.timedelta(days = 1)
 
    times = pd.date_range(f"{date} 21:00", 
                          f"{date + delta} 07:00", 
                          freq = "10min")
    
    
        
    fig = plt.figure(figsize = (22, 10))
    
    plt.subplots_adjust(wspace = 0.2, hspace = 0.5)
    
    G = gridspec.GridSpec(3, 3)
    
    
    ax1 = plt.subplot(G[0, :])
    
    df = load_and_plot_roti(ax1, infile_from_date(date), 
                            times[0], times[-1])
    
    
    
    shade(ax1, df, date_from_filename(tecFilename).datetime, 
          threshold = 1)
    
    
    ax2 = plt.subplot(G[1:, -1], projection = ccrs.PlateCarree())
    
    plotTECmap(ax2, os.path.join(infile, "tec\\"), tecFilename)
    
    
    ax3 = plt.subplot(G[1:, 0])
    
    
    if imagerFilename == None:
    
        ax3.text(0.15, 0.5, "Sem imagens", transform = ax3.transData, 
                 color = "red", fontsize = 40)
        
        plot_image(None, ax3)
        name = date_from_filename(tecFilename).datetime
        name += datetime.timedelta(minutes = num_time)
        
    else:
        img = load_and_processing(os.path.join(infile, "imager", 
                                                    imagerFilename))
        plot_image(img, ax3)
    
        draw_labels(ax3, imagerFilename, fontsize = 18, 
                    color = "white")
        
        name = date_from_filename(imagerFilename).datetime
    
    ax4 = plt.subplot(G[1:, -2])
        
    plot_image(crop_image(os.path.join(infile, 
                                       f"ionosonde\\{ionoFilename}")), ax4)
    
    
    ax4.set(ylabel = "Altura (km)", xlabel = "Frequência (Hz)", 
            title =  date_from_filename(tecFilename).datetime)
    
    x = 0.3
    y = -0.15
    
    labels = ["Mapa de TEC (Brasil)", 
              "Imageador (Cariri)", 
              "Digissonda (Fortaleza)"]
    
    
    for num, ax in enumerate([ax2, ax3, ax4]):
    
        ax.text(x, y, labels[num], transform = ax.transAxes)            
  
    
    locale.setlocale(locale.LC_ALL, 'pt_pt.UTF-8')
    day1 = date.strftime('%d')
    day2 = (date + delta).strftime('%d')
    fig.suptitle(f"Observações: {day1}-{day2} de {date.strftime('%B')} de {date.year}", 
                 y = 0.94)
    
    
    if save:
        print("Saving...", name)
        name_to_save = name.strftime("%Y%m%d%H%M%S") 
        fig.savefig(f"{path_to_save}\\{name_to_save}.png", 
                   dpi = 100, bbox_inches="tight")
        
        plt.clf()   
        plt.close()
    else:
        plt.show()
        
        


 
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
            
            
#run_for_all_day(date, image_files, tec_files, iono_files, infile)

def make_dir(infile):
    """Create a new directory by path must be there year and doy"""
    
    path_to_create = os.path.join(infile, "joined")
    
    
    try:
        os.mkdir(path_to_create)
        
        print(f"Creation of the directory {path_to_create} successfully")
        
    except OSError:
        print(f"Creation of the directory {path_to_create} failed")
      
   
    return path_to_create


path_root = "C:\\Users\\Public\\observation\\"

_, folders, _  = next(os.walk(path_root))

year = 2014
for folder in folders:
    
    if folder == "225":
    
        date = datetime.date(year, 1, 1) + datetime.timedelta(int(folder) - 1)
        
        
        infile = os.path.join(path_root, folder)
        
        
        image_files = get_files(os.path.join(infile, "imager"))
        
        
        tec_files = get_files(os.path.join(infile, "tec"))
        
        
        iono_files = get_files(os.path.join(infile,"ionosonde"), 
                           extension = ".PNG")
        
        path_to_save = make_dir(infile)
        
        try:
            run_for_all_day(date, image_files, tec_files, 
                        iono_files, infile, path_to_save)
            
        except:
            print(folder, "não deu")
            continue
#
"""
out = ordering(date, image_files)
num = 10
tecFilename, ionoFilename, imagerFilename = tuple(out[num])

plot_quadri_observation(date, 
                 infile,  
                 imagerFilename, 
                 ionoFilename, 
                 tecFilename, 
                 save = False, 
                 path_to_save = path_to_save,
                 num_time = 0)
"""