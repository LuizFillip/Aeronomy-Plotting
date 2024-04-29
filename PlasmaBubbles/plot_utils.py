import matplotlib.pyplot as plt 

def legend_max_points_roti(
        ax, 
        fontsize = 30, 
        s = 100, 
        threshold = 0.25
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
    

    labels = [
        'ROTI points',
        'Maximum value', 
        f'{threshold} TECU/min'
        ]

    plt.legend(
        [l1, l2, l3], 
        labels, 
        ncol = 1, 
        fontsize = fontsize,
        bbox_to_anchor = (1.07, 1.2),
        handlelength = 2,
        loc = 'upper right',
        borderpad = 1.8,
        handletextpad = 1, 
        scatterpoints = 1
        )
