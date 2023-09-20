import cv2
import os
import matplotlib.pyplot as plt
import digisonde as dg


def crop_image(img, y = 50, x = 130, h = 900, w = 750):
    
    return img[y: y + h, x: x + w]

def plot_ionogram(ax, infile, crop = True):

    img = cv2.imread(infile)

    if crop:
        img = crop_image(img) 

    ax.imshow(img)
    
    filename = os.path.split(infile)[-1]
    dn = dg.ionosonde_fname(filename)
    
    
    ax.set(title = dn.strftime("%d/%m %H:%M"))
    
    ax.axis("off")
    
    return ax
        

def plot_sequence():
        
    fig, ax = plt.subplots(
         figsize = (12, 11), 
         dpi = 300, 
         ncols = 5, 
         nrows = 3
         )
    
    plt.subplots_adjust(wspace = 0)
    
    site = "Sao Luis"
    
    if site == "Sao Luis":
        folder = "saa"
    else:
        folder = "fza"
    
    infile = f"D:\\iono\\ionograms_20130317\\{folder}\\"
    
    files = ['FZA0M_20130316(075)220000.PNG', 'FZA0M_20130316(075)230000.PNG', 
             'FZA0M_20130317(076)000000.PNG', 'FZA0M_20130317(076)010000.PNG', 
             'FZA0M_20130317(076)020000.PNG', 'FZA0M_20130317(076)220000.PNG', 
             'FZA0M_20130317(076)230000.PNG', 'FZA0M_20130318(077)000000.PNG', 
             'FZA0M_20130318(077)010000.PNG', 'FZA0M_20130318(077)020000.PNG', 
             'FZA0M_20130318(077)222000.PNG', 'FZA0M_20130318(077)230000.PNG', 
             'FZA0M_20130319(078)000000.PNG', 'FZA0M_20130319(078)011000.PNG', 
             'FZA0M_20130319(078)020000.PNG']
    
    
    for num, ax in enumerate(ax.flat):
        filename = files[num].replace("FZA0M", "SAA0K")
    
        plot_ionogram(ax, infile + filename)
    fontsize = 30
    fig.text(.07, 0.4, "Altitude (km)", rotation = "vertical", fontsize = fontsize)
    fig.text(.4, 0.07, "Frequência (MHz)", fontsize = fontsize)
    
    fig.suptitle(site, y = 0.97, fontsize = fontsize)
    fig.savefig(f"digisonde/src/figures/ionograms_{site.lower()}.png", dpi = 300)
    plt.show()


