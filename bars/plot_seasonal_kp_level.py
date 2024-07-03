import matplotlib.pyplot as plt 
import base as b
import core as c
import PlasmaBubbles as pb 


b.config_labels(fontsize = 30)

def plot_seasonal_kp_level(
        df,
        level = -30, 
        translate = True
        ):
    
    if translate:
        ylabel = 'Number of nights'
        xlabel = 'Months'
        ln = 'en'
    else:
        ylabel = 'Número de casos'
        xlabel = 'Meses'
        ln = 'pt'
    
    fig, ax = plt.subplots(
        nrows = 2, 
        dpi = 300,
        sharey = True,
        sharex = True,
        figsize = (18, 14)
        )
    
    plt.subplots_adjust(hspace = 0.2)
    
    DL = c.DisturbedLevels(df)

    names = DL.geomagnetic_labels(level, dst = True)
    
    for i, ds in enumerate(DL.Dst(level = level)):
        
        data = c.count_occurences(ds).month
        data = data.iloc[:, :4]
        
        data.plot(
            kind = 'bar',
            ax = ax[i], 
            legend = False,
            edgecolor = 'k'
            )
    
        ax[i].set(
            ylabel = ylabel,
            xlabel = xlabel,
            xticklabels = b.month_names(language = ln)
            )
        
        
        summations = data.sum().values[:4]
        
        t = [f'Setor {i} ({int(v)})' for i, v in
             enumerate(summations, start = 1)]        
        
        ax[i].legend(
            t,
            ncol = 5, 
            
            bbox_to_anchor = (.5, 1.22), 
            loc = "upper center", 
            columnspacing = 0.3,
            fontsize = 28
            )
    
        
    plt.xticks(rotation = 0)
    
    b.add_lines_and_letters(
            ax, 
            names, 
            fontsize = 40,
            x = 0.02, 
            y = 0.85, 
            num2white = None
            )
    
    return fig


def main():
    df = b.load(
        'events_class2')
    ds = pb.sel_typing(df, typing = 'midnight', 
    indexes = True, 
    year = 2023)
    
    
    fig = plot_seasonal_kp_level(ds, translate = False)
    
    # fig.savefig(b.LATEX('Kp_seasonal_variation'))


main()