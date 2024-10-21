import matplotlib.pyplot as plt
import numpy as np

def draw_neural_network(layers):
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
    
    labels = ['F10.7', 'SYM-H', 'h`F2', 
              'Convecção', 'Dia do ano']
    for i, y in enumerate(positions):
        
        
        ax.text(
            -0.5, y, 
            labels[i],
            fontsize = 25, 
            ha = 'center', 
            va = 'center', 
            color = 'black'
            )
        
    ax.text(
        3.5, 0, 
        'saída',
        fontsize = 25, 
        ha = 'center', 
        va = 'center', 
        color = 'black'
        )
    
    
    def plot_rectangle(
            ax, 
            x0, x1, 
            y0 = -5, 
            y1 = 5, 
            color = 'lime'
            ):
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
        
    plot_rectangle(
            ax, 
            -0.15, 0.15
            )
    
    plot_rectangle(
            ax, 
            0.7, 2.2, 
            color = 'lightblue'
            )
    
    plot_rectangle(
            ax, 
            2.8, 3.2, 
            color = 'red'
            )

    return fig 

# Exemplo: rede neural com 3 neurônios na entrada, 4 e 3 neurônios em duas camadas ocultas, e 2 neurônios na saída
layers = [5, 6, 4, 1]
fig = draw_neural_network(layers)
