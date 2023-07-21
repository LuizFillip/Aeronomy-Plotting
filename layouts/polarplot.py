import matplotlib.pyplot as plt
import numpy as np
import random as r


def circle(ax, limit, step):
    
    for cir in range(0, int(limit), step):
    
        circle = plt.Circle((0, 0),
                            cir, 
                            color='k', 
                            linestyle = "--",
                            fill = False)
        ax.add_patch(circle)

def arrow(ax, radius, angle):
    
    x = radius * np.cos(np.radians(angle))
    y = radius * np.sin(np.radians(angle))
    
    ax.annotate("",
                xy=(x, y), 
                xycoords = 'data',
                xytext=(0, 0), 
                textcoords='data',
                arrowprops=dict(arrowstyle="->",
                                lw = 3, 
                                connectionstyle="arc3"),
                ) 


def duplicate_axes(ax):
    
    
    ax1 = ax.twinx()
    ax1.yaxis.set_ticks_position('left')
    ax2 = ax.twiny()
    ax2.xaxis.set_ticks_position("bottom")
    ax1.set(ylim = ax.get_ylim())
    ax2.set(xlim = ax.get_xlim())    
    
    
    
def polarplot(ax, radius, angle, step = 50):

    ax.spines.left.set_position('zero')
    ax.spines.right.set_color('none')
    ax.spines.bottom.set_position('zero')
    ax.spines.top.set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
        
    

    for radius, angle in zip(speed, phase):
        arrow(ax, radius, angle)

    limit = max(speed) + step
    
    ax.text(0, limit, "N")
    
    
    ax.set(ylim = [-limit, limit],
           xlim = [-limit, limit], 
           xticks = [], 
           yticks = [])
    
    duplicate_axes(ax)
    
    circle(ax, limit, step)
    
     
fig, ax = plt.subplots(figsize = (10, 10))


N = 50
speed = [r.randint(0, 300) for p in range(0, N)]
phase = [r.randint(0, 360) for p in range(0, N)]

polarplot(ax, speed, phase)  


ax.set(ylabel = "Speed (m/s)")
