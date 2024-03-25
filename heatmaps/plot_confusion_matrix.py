
import matplotlib.pyplot as plt
import numpy as np

# Example confusion matrix data
conf_matrix = np.array([[20, 5],
                        [2, 25]])

# Define labels for observations and forecast indices
observation_labels = ['sim', 'não']
forecast_labels = ['sim', 'não']

# Plotting the confusion matrix
plt.imshow(conf_matrix, interpolation='nearest', cmap=plt.cm.Blues)

plt.colorbar()

# Add annotations
for i in range(conf_matrix.shape[0]):
    for j in range(conf_matrix.shape[1]):
        plt.text(j, i, str(conf_matrix[i, j]), horizontalalignment='center', verticalalignment='center', color='white')


plt.xticks(np.arange(conf_matrix.shape[1]), forecast_labels)
plt.yticks(np.arange(conf_matrix.shape[0]), observation_labels)

plt.ylabel('Observação')
plt.xlabel('Previsão')

plt.tick_params(axis='x', labeltop=True, labelbottom=False)

plt.gca().xaxis.set_label_position('top')


plt.show()

