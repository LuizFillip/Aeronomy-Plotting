import matplotlib.pyplot as plt 

def legend_max_points_roti(
        ax, 
        fontsize = 25, 
        s = 100, 
        threshold = 0.25,
        anchor = (1.07, 1), 
        ncol = 1, 
        translate = True
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
    
    if translate:
        
        labels = [
            'ROTI points',
            'Maximum value', 
            f'{threshold} TECU/min'
            ]
    else:
        labels = [
            'Pontos de ROTI',
            'Valor máximo', 
            f'{threshold} TECU/min'
            ]

    plt.legend(
        [l1, l2, l3], 
        labels, 
        ncol = ncol, 
        fontsize = fontsize,
        bbox_to_anchor = anchor,
        columnspacing = 0.3,
        loc = 'upper center'
        )
    
def plot_terminator():
    
    return 
