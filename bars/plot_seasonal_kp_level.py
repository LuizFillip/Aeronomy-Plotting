import matplotlib.pyplot as plt 
import base as b
import core as c
import PlasmaBubbles as pb 


b.config_labels()

def plot_seasonal_kp_level(
        df,
        kp_level = 3
        ):
    
    fig, ax = plt.subplots(
        nrows = 2, 
        dpi = 300, 
        sharex = True,
        figsize = (14, 10)
        )
    
    plt.subplots_adjust(hspace = 0.2)
    
    datasets = c.DisturbedLevels(df).Kp(level = kp_level)

    names = [f'$Kp \\leq$ {kp_level}',  f'$Kp >$ {kp_level}']
    
    for i, ds in enumerate(datasets):
        
        data = c.count_occurences(ds).month
        data = data.iloc[:, :4]
        
        data.plot(
            kind = 'bar',
            ax = ax[i], 
            legend = False,
            edgecolor = 'k'
            )
    
        ax[i].set(
            ylim = [0, 100],
            ylabel = 'Number of nights',
            xlabel = 'Months',
            xticklabels = b.number_to_months()
            )
        
        
        summations = data.sum().values[:4]
        
        t = [f'{i + 1} ({int(v)})' for i, v in
             enumerate(summations)]        
        
        ax[i].legend(
            t,
            ncol = 5, 
            loc = "upper center", 
            columnspacing = 0.6
            )
    
        
    plt.xticks(rotation = 0)
    
    b.add_lines_and_letters(
            ax, 
            names, 
            fontsize = 25,
            x = 0.0, 
            y = 1.05, 
            num2white = None
            )
    
    return fig


def main():
    df = b.load('events_class2')
    ds = pb.sel_typing(df, typing = 'midnight')
    
    
    fig = plot_seasonal_kp_level(ds)
    
    # fig.savefig(b.LATEX('Kp_seasonal_variation'))


