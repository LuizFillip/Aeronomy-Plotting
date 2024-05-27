import imager as im
import matplotlib.pyplot as plt 
import numpy as np 
import base as b

b.config_labels()

def velocity(time, distance):
    delta_d = (distance[-1] - distance[0]) 
    delta_t = (time[-1] - time[0])
    return round((delta_d / delta_t) / 3.6, 2)

def plot_vel_info(ax, time_1, dist_1, line1):
    
    vel_1 = velocity(time_1, dist_1)
    
    ax.text(time_1[-1], dist_1[-1] - 60,
            f'{vel_1} m/s', 
            color = line1.get_color())



def plot_velocities(ax):
    
    time_1, dist_1 = [26.3, 28], [50, 400]
    time_2, dist_2 = [25, 28], [400, -20]
    time_3, dist_3 = [28, 29], [-20, 150]

    
    line1, = ax.plot(time_1, dist_1, lw = 2, color = 'b')
    line2, = ax.plot(time_2, dist_2, lw = 2, color = 'r')
    line3, = ax.plot(time_3, dist_3, lw = 2, color = 'w')
    
    
    plot_vel_info(ax, time_1, dist_1, line1)
    plot_vel_info(ax, time_2, dist_2, line2)
    plot_vel_info(ax, time_3, dist_3, line3)


def plot_keogram(
        zonal, 
        merid, 
        extent, 
        date,
        ytick = 200, 
        layer = 'O6', 
        site = 'BJL', 
        cmap = 'Greys_r'
        ):

    fig, ax = plt.subplots(
            figsize = (12, 10), 
            nrows = 2,
            dpi = 300,
            sharex = True, 
            sharey = True, 
     )

    plt.subplots_adjust(hspace = 0.05)
    
    
    ax[0].imshow(
        zonal, 
        aspect = 'auto', 
        extent = extent,
        cmap = cmap
        )
    ax[1].imshow(
        merid, 
        aspect = 'auto', 
        extent = extent,
        cmap = cmap
        )
    
    ax[0].text(
        0, 1.02, 
        site, 
        transform = ax[0].transAxes)
    ax[0].text(
        0.95, 1.02, 
        layer, 
        transform = ax[0].transAxes)
    
    step =  keo.y_limit() / 2
    yticks = np.arange(-ytick, ytick + step, step)
    xticks = np.arange(round(extent[0]), 
                       round(extent[1]) + 1, 1)    
    ax[0].set(
        ylabel = 'Zonal (W-E)', 
        yticks = yticks, 
        title = date
        )
    ax[1].set(
        xticks = xticks,
        ylabel = 'Meridional (N-S)', 
        yticks = yticks, 
        xlabel = 'Universal time'
        )
    
    for a in ax.flat:
        a.axhline(0, lw = 2, color = 'w', linestyle = '--')
        
    return fig, ax


infile = 'database/images/CA_2013_1224/'
# infile = 'database/images/CA_2022_0724/'
infile = 'database/images/BJL_2022_0724/'
# infile = 'D:/images/CA_2014_0102/'


area_factor = 2

keo = im.KeogramAnalysis(infile, area_factor = area_factor)

zonal, merid = keo.make_keo(limits = [0.25, 0.95])

fig, ax = plot_keogram(
        zonal, 
        merid, 
        extent = keo.extend_values(), 
        date = keo.date, 
        ytick = keo.y_limit(), 
        layer = keo.layer, 
        site = keo.site, 
        cmap = 'Greys_r'
        )



# plot_velocities(ax[0])