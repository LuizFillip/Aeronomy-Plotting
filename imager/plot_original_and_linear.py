import imager as im 
import matplotlib.pyplot as plt 


path_of_image = 'database/images/BJL_2022_0724/O6_BJL_20220725_031605.tif'

area_factor = 2
 
all_sky = im.processing_img(path_of_image)

areap = 512 * area_factor

img = all_sky.linear(all_sky.bright(), area = areap)

fig, ax = plt.subplots(
    figsize = (12, 8), 
    dpi = 300, 
    ncols = 2
    )


im.plot_images(
        path_of_image, 
        ax[0], 
        flip = True, 
        infos = True, 
        time_infos = False, 
        fontsize = 20,
        limits = [0.3, 0.95],
        dt_ps = (395, 510)
        )


ax[1].imshow(
    img,
    cmap = 'gray'    
    )