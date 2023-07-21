import matplotlib.pyplot as plt

def remove_lines(ax, nrows, ncols):
    
    '''
    Remove inferior and superior lines (spines) from the subplots
    with the exception the firt (must have the top spine)
    and the last one, must have the bottom, only. 
    
    Parameters 
    '''

    if (ncols > 1) and (nrows > 1): 
        for x in range(nrows):
            for y in range(ncols):
                if y == 0:
                    ax[x, y].spines['right'].set_visible(False)
                    if x == 0: 
                        ax[x, y].spines['bottom'].set_visible(False)
                    elif x == (nrows - 1):
                        ax[x, y].spines['top'].set_visible(False)   
                    else:
                        ax[x, y].spines['top'].set_visible(False)   
                        ax[x, y].spines['bottom'].set_visible(False)  
                        
                else:
                    ax[x, y].spines['left'].set_visible(False)
                    if x == 0: 
                        ax[x, y].spines['bottom'].set_visible(False)
                        ax[x, y].axes.yaxis.set_visible(False)
                    elif x == (nrows - 1):
                        ax[x, y].spines['top'].set_visible(False)   
                        ax[x, y].axes.yaxis.set_visible(False)
                    else:
                        ax[x, y].spines['top'].set_visible(False)   
                        ax[x, y].spines['bottom'].set_visible(False)  
                        ax[x, y].axes.yaxis.set_visible(False)
                        
    elif (ncols == 1) and (nrows > 1):
        
        for num in range(nrows):
            if num == 0:    
                ax[num].spines['bottom'].set_visible(False)       
            elif num == (nrows - 1):    
                ax[num].spines['top'].set_visible(False)
                
            else:
                ax[num].spines['top'].set_visible(False)
                ax[num].spines['bottom'].set_visible(False)
                
    else:
        
        for num in range(ncols):
            if num == 0:    
                ax[num].spines['right'].set_visible(False)  
                
            elif num == (ncols - 1):    
                ax[num].spines['left'].set_visible(False)
                ax[num].axes.yaxis.set_visible(False)
                
            else:
                ax[num].spines['left'].set_visible(False)
                ax[num].spines['right'].set_visible(False)
                ax[num].axes.yaxis.set_visible(False)
                
                
                
def main():
    
    scopes = [(3, 1), (1, 3), (3, 3)]
    
    for num in scopes:
        
        fig, ax = plt.subplots(figsize = (6, 6), 
                               sharex = True, 
                               sharey = True,
                               nrows = num[0], 
                               ncols = num[1])
        
        plt.subplots_adjust(hspace = 0, wspace = 0)
        
        remove_lines(ax, nrows = num[0], ncols = num[1])
        
        
main()