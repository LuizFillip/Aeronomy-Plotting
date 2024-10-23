import matplotlib.pyplot as plt
import numpy as np
import base as b 

b.config_labels()

def plot_rectangle(
        ax, 
        x0, x1, 
        y0 = -5, 
        y1 = 5, 
        color = 'lime'
        ,name = ''):
    rect = plt.Rectangle(
        (x0, y0), 
        x1 - x0, 
        y1 - y0,
        edgecolor = 'k', 
        facecolor = color, 
        linewidth = 1, 
        alpha = 0.3
        )
    
    ax.add_patch(rect)
    middle = x0 + (x1 - x0)/ 2
    ax.text(
        middle, 
        y1 + 0.5, 
        name,
        fontsize = 25, 
        ha = 'center', 
        va = 'center', 
        color = 'black'
        )
def draw_neural_network(layers, labels):
    fig, ax = plt.subplots(dpi = 300, figsize=(10, 6))
    ax.axis('off')  # Remove os eixos
    
    neuron_positions = []
    v_spacing = 1.5  # Espaçamento vertical entre os neurônios
    h_spacing = 1  # Espaçamento horizontal entre as camadas

    for i, n_neurons in enumerate(layers):
        layer_x = i * h_spacing
        layer_y = np.linspace(
            -v_spacing * (n_neurons - 1) / 2,
            v_spacing * (n_neurons - 1) / 2, n_neurons)
        neuron_positions.append((layer_x, layer_y))
    
    offset = 0.1
    for i in range(len(layers) - 1):
        layer1_x, layer1_y = neuron_positions[i]
        layer2_x, layer2_y = neuron_positions[i + 1]
        
        for x1, y1 in zip(layer1_x * np.ones(len(layer1_y)), layer1_y):
            for x2, y2 in zip(layer2_x * np.ones(len(layer2_y)), layer2_y):
                ax.plot(
                    [x1 + offset, x2 - offset], 
                    [y1, y2], 'k', lw = 0.5
                    )  
 
    
    for x, y in neuron_positions:
        ax.scatter(
            x * np.ones(len(y)), y,
            s = 1000, 
            zorder = 3, 
            facecolor = 'gray', 
            alpha = 0.5, 
            edgecolor = 'k', 
            lw = 2
            )
    
    index, positions = neuron_positions[0]
    
    for i, y in enumerate(positions):
        
        
        ax.text(
            -0.7, y, 
            labels[i],
            fontsize = 25, 
            ha = 'center', 
            va = 'center', 
            color = 'black'
            )
        
   
    
    y1 = len(layers)

        
    plot_rectangle(
            ax, 
        
            -0.15, 0.15, 
            
            y0 = -y1, 
            y1 = y1,
            name = 'Entrada'
            )
    
    plot_rectangle(
            ax, 
            0.7, 3.2, 
            y0 = -y1, 
            y1 = y1,
            color = 'lightblue', 
            name = 'Modelos'
            )
    
    plot_rectangle(
            ax, 
            3.8, 4.2, 
            y0 = -y1, 
            y1 = y1,
            color = 'red', 
            name = 'Saída'
            )

    return fig 


def main():
    labels = ['F10.7', 'SYM-H', '$V_z$',
                  'Convecção', 'Dia do ano']
    
    num = len(labels)
    layers = [num, num + 1, num + 2, num + 1, 1]
    fig = draw_neural_network(layers, labels)
    FigureName = 'RedeNeural'
    fig.savefig(
        b.LATEX(FigureName, 'posdoc'),
        dpi = 400
        )
    
    
