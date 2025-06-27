
def arrow(ax, xy, xytext, text = '$B_1$', color = 'red'):

    ax.annotate(
        text, xy = xy, 
        xytext=xytext,
        arrowprops=dict(
            color = color,
            lw = 4,
            arrowstyle='->'), 
        transform = ax.transData, 
        fontsize = 40, 
        color = color
        )
    return None 

def plot_arrows_bubbles(axs):
    arrow(axs[0, 1], (-60, -10), (-60, 10), text = '$B_1$')
    arrow(axs[0, 2], (-55, -10), (-55, 10), text = '$B_1$')
    arrow(axs[0, 2], (-65, -10), (-65, 10), text = '$B_2$', 
          color = 'black')
    
    arrow(axs[1, 0], (-50, -10), (-50, 10), text = '$B_1$')
    arrow(axs[1, 0], (-65, -10), (-65, 10), text = '$B_2$', 
          color = 'black')
    
    arrow(axs[1, 1], (-47, -8), (-47, 11), text = '$B_1$')
    arrow(axs[1, 1], (-60, -10), (-60, 10), text = '$B_2$', 
          color = 'black')
    
    arrow(axs[1, 2], (-45, -8), (-45, 11), text = '$B_1$')
    arrow(axs[1, 2], (-58, -10), (-58, 10), text = '$B_2$', 
          color = 'black')
    
    return None 
      