
import matplotlib.pyplot as plt
import numpy as np
import core as c 


def plot_matrix(ax, conf_matrix):
    
# Plotting the confusion matrix
    ax.imshow(conf_matrix, cmap= 'magma')
    
    
    # Add annotations
    for i in range(conf_matrix.shape[0]):
        for j in range(conf_matrix.shape[1]):
            if i == 1 and j == 1:
                color = 'k'
            else:
                color = 'w'
            ax.text(j, i, str(conf_matrix[i, j]),
                    horizontalalignment='center', 
                     verticalalignment='center', 
                     color= color, fontsize = 50)
    
    ax.set(ylabel = 'Observação', xlabel = 'Previsão', 
           xticks = np.arange(conf_matrix.shape[1]), 
           yticks = np.arange(conf_matrix.shape[0]), 
           xticklabels = forecast_labels, 
            yticklabels = observation_labels)
    
    
    # ax.tick_params(axis='x', labeltop=True, labelbottom=False)
    
    

# Define labels for observations and forecast indices
observation_labels = ['Com EPB', 'Sem EPB']
forecast_labels = ['Com EPB', 'Sem EPB']

fig, ax = plt.subplots(
    dpi = 300, 
    figsize = (14, 10),
    ncols = 2)

plt.subplots_adjust(wspace = 0.5)


def plot_results(ax, precision = True):
    
    fore = c.forecast_epbs(year_threshold = 2023, parameter= 'vp')
    
    if precision:
        precision = fore.accuracy_score
        
        ax.set(title = '$V_P$ - ' + f'Precisão {precision} \%')
    
    conf_matrix = fore.confusion_matrix
    
    plot_matrix(ax, conf_matrix)


fore = c.forecast_epbs(year_threshold = 2023, parameter= 'gamma')

conf_matrix = fore.confusion_matrix
precision =  round(fore.accuracy_score, 2) * 100


ax[1].set(title = '$\gamma_{RT}$ - ' + f'Precisão {precision} \%')


plot_matrix(ax[1], conf_matrix)

