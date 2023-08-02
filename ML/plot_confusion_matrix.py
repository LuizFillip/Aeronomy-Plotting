import seaborn as sn
import matplotlib.pyplot as plt
import pandas as pd

def plot_confusion_matrix(cm):
    
    fig, ax = plt.subplots(figsize = (8, 8))
    
    names = ['non-EPB', 'EPB']
    
    df_cm = pd.DataFrame(
        cm, 
        index = names,
        columns = names
        )
    
    
    sn.heatmap(df_cm, annot=True)
# plot_confusion_matrix()