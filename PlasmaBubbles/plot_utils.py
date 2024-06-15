import matplotlib.pyplot as plt 

def legend_max_points_roti(
        ax, 
        fontsize = 30, 
        s = 100, 
        threshold = 0.25,
        anchor = (1.07, 1), 
        ncol = 1
        ):
    
    l1 = plt.scatter(
        [], [], 
        color = 'gray', 
        marker = 'o', 
        s = s
        )
    
    l2 = plt.scatter(
        [], [], 
        color = 'black', 
        marker = 'o', 
        s = s
        )
    
    l3 = ax.axhline(
        threshold, 
        color = 'red', 
        lw = 2
        )
    
    # l4 = ax.axhline(
    #     threshold, 
    #     color = 'k', 
    #     lw = 2
    #     )
    
    # l5 = ax.axhline(
    #     threshold, 
    #     color = 'k', 
    #     lw = 2,
    #     linestyle = '--'
    #     )

    labels = [
        'ROTI points',
        'Maximum value', 
        f'{threshold} TECU/min',
        # 'Solar terminator (300 km)', 
        # 'Local midnight'
        ]

    plt.legend(
        [l1, l2, l3], #, l4, l5], 
        labels, 
        ncol = ncol, 
        fontsize = fontsize,
        bbox_to_anchor = anchor,
        handlelength = 2,
        loc = 'upper center',
        borderpad = 1.8,
        handletextpad = 1, 
        scatterpoints = 1
        )
    
def plot_terminator():
    
    return 
