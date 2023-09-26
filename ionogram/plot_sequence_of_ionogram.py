import cv2
import os
import matplotlib.pyplot as plt
import digisonde as dg

PATH_IONOGRAM = 'database/iono/20170329/'

def crop_image(
        img, 
        y = 50, 
        x = 130, 
        h = 900, 
        w = 750
        ):
    
    return img[y: y + h, x: x + w]

def plot_ionogram(
        ax, 
        infile, 
        crop = True, 
        format_ = '%H:%M'
        ):

    img = cv2.imread(infile)

    if crop:
        img = crop_image(img) 

    ax.imshow(img)
    
    filename = os.path.split(infile)[-1]
    dn = dg.ionosonde_fname(filename)
    
    ax.set(title = dn.strftime(format_))
    
    ax.axis("off")
    
    return dn
        
def fig_labels(
        fig, 
        fontsize = 30, 
        title = ''
        ):


    fig.text(
        .07, 0.4, 
        "Altitude (km)", 
        rotation = "vertical", 
        fontsize = fontsize
        )
    
    fig.text(
        .4, 0.07, 
        "Frequência (MHz)",
        fontsize = fontsize
        )
    
    fig.suptitle(
        title, 
        y = 1.03, 
        fontsize = fontsize
        )
    

def plot_sequence_of_ionogram():
    
    fig, ax = plt.subplots(
         figsize = (12, 7), 
         dpi = 300, 
         ncols = 5, 
         nrows = 2
         )
    
    plt.subplots_adjust(wspace = 0)
    
    files = os.listdir(PATH_IONOGRAM)
    
    files = sorted([f for f in files if 'PNG' in f])
    
    # files = files[2:]
    for i, ax in enumerate(ax.flat):
        
        fname = files[i]
        
        infile = os.path.join(
            PATH_IONOGRAM, 
            fname
            )
        
        dn = plot_ionogram(
            ax, 
            infile, 
            crop = True
            )
        
        
        if 'SAA' in fname:
            site = "Sao Luis"
            
        elif 'BVJ' in fname:
            site = 'Boa vista'
            
        else:
            site = "Fortaleza"
            
    date = dn.strftime('%d/%m/%Y')
    title = f'{site} - {date}'
    
    fig_labels(
        fig, 
        fontsize = 30, 
        title = title
        )
    
    return

plot_sequence_of_ionogram()