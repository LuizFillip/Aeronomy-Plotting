import PlasmaBubbles as pb 
import matplotlib.pyplot as plt  
import base as b 
 


path = 'database/epbs/class_r/2014.txt'

df =  pb.types_dataset(path)

df = df.iloc[:, 0:5]

df = df.replace(2, 1)


ds = pb.month_occurrence(
        df, 
        value = 1
        )

def plot_seasonal_byreceivers(ds):
   
    
    fig, ax = plt.subplots(
        figsize = (12, 6), 
        dpi = 300
        )
    
    ds.plot(kind = 'bar', ax = ax)
    
    ax.set( xticklabels = b.number_to_months(), 
           xlabel = 'Meses', ylabel = 'Noites com EPBs')
    
    
    ax.legend(
        ncol = 5, 
        title = 'Numero de receptores',
        bbox_to_anchor = (.5, 1.2), 
        loc = "upper center", 
        columnspacing = 0.6
        )
    
    plt.xticks(rotation = 0)
     