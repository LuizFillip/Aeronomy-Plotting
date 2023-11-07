import matplotlib.pyplot as plt
import numpy as np
import results as r



def plot_frequency_rate(epb_infile, col = 'salu', year = 2013):
    
    """Plotting annual EPBs occurrence like histogram"""
    
    df = r.monthly_occurrence(epb_infile, col = col)
    
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (10, 5)
        )
    
    args = dict(facecolor='lightgrey', 
                alpha=1, 
                
                edgecolor = 'black',  
                color = 'gray', 
                width = 1)
       
    df.index = np.arange(1, 13, 1)
        
    df["percent"].plot(kind = 'bar', **args)
    
    
    ax.set(ylabel = "Rate (\%)", 
           xlabel = f"Months ({year})",
           ylim  = [0, 20], 
           )

    
    ax.tick_params(axis = 'x', labelrotation = 0)
    
  
    return df
    
def main():
    
    epb_infile = 'database/Results/EPBs_ROTI/epbs_2015.txt'
    
    plot_frequency_rate(epb_infile, col = 'roti', year = 2014)
    # df.to_csv(epb_infile)
# main()