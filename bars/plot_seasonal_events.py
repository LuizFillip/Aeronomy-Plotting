import core as c
import matplotlib.pyplot as plt
import base as b 
import PlasmaBubbles as pb 


b.config_labels(blue = False, fontsize = 35)



def plot_seasonal_occurrence(
        ds, 
        typing = 'sunset', 
        translate = False
        ):
    
    e_year = ds.index[-1].year
    s_year = ds.index[0].year

    
    if typing == 'sunset':
        vmax = 350
        if translate:
            typing = 'pós-pôr do sol'
        else:
            typing = 'Sunset'
        
    else:
        vmax = 160
        if translate:
            typing = 'pós-meia-noite'
        else:
            typing = 'post-midnight'
        
    
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (18, 8)
        )
            
    df = c.count_occurences(ds).month
    # df = df[df.columns[::-1]]
    df = df[[-50, -60, -70]]
    
    df.plot(
        kind = 'bar', 
        edgecolor = 'k',
        ax = ax, 
        legend = False
        )

    plt.xticks(rotation = 0)
    
    if translate:
        ylabel = 'Número de casos'
        xlabel = 'Meses'
        sector = 'Setor'
        title = f'Eventos de EPBs {typing} ({s_year} - {e_year})'
        language = 'pt'
    else:
        ylabel = 'Number of cases'
        xlabel = 'Months'
        sector = 'Sector'
        title = f'Events of {typing} EPBs ({s_year} - {e_year})'
        language = 'en'
    
    ax.set(
        ylabel = ylabel,
        xlabel = xlabel,
        xticklabels = b.month_names(
            sort = True, language = language),
        ylim = [0, vmax]
        )
        
    t = [f'{sector} {i} ({vl})' for i, vl in 
         enumerate(df.sum().values, start = 1)]
    
    ax.legend(
        t,
        ncol = 5, 
        title = title,
        bbox_to_anchor = (.5, 1.3), 
        loc = "upper center", 
        columnspacing = 0.3,
        fontsize = 30
        )
    
    return fig
    
    
    

def main():

    df = b.load('features_one_hour')
    df = b.load('events_class2')
    # df = df.loc[df.index.year < 2023]
    translate = False
    
    for typing in ['sunset', 'midnight']:

        ds = pb.sel_typing(df, typing = typing)
        
    
        fig = plot_seasonal_occurrence(
            ds, typing, translate = translate)
        if translate:
            FigureName = f'pt/seasonal_{typing}'
        else:
            FigureName = f'en/seasonal_{typing}'
              
        fig.savefig(
              b.LATEX(FigureName, folder = 'bars'),
              dpi = 400
              )
    # # 
main()

# df = b.load('events_class2')



# df.loc[(df['lon'] == -50) & 
#        (df.index.year == 2018) & 
#        (df.index.month == 12)]
