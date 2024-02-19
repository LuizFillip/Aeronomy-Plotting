import base as b 
import matplotlib.pyplot as plt 
import core as c
import plotting as pl 



b.config_labels(fontsize = 25)

    
def save_figs(df, col = 'gamma'):
    
    names = ['seasonal_quiet', 
             'seasonal_disturbed']
    
    title = ['$Kp \\leq 3$',  '$Kp > 3$']

    for i, FigureName in enumerate(names):
    
        if 'quiet' in FigureName:
            df1 = df.loc[df['kp'] <= 3]
        else:
            df1 = df.loc[df['kp'] > 3]
        
        fig = plot_distributions_seasons(df1, col)
        
        fig.suptitle(title[i], y = 0.95)
        
        fig.savefig(
            b.LATEX(FigureName),
            dpi = 400
            )


def FigureLabels(
        fig, 
        translate = False, 
        fontsize = 30
        ):
    if translate:
        ylabel1 = "Probabilidade de ocorrência (\%)"
        ylabel2 = "Frequência de ocorrência"
       
    else:
        ylabel1 = "EPB occurrence probability"
        ylabel2 = "Frequency of occurrence"
        
    fig.text(
        0.07, 0.33, 
        ylabel1, 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.49, 0.37, 
        ylabel2, 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.45, 0.07, 
        b.y_label('gamma'), 
        fontsize = fontsize
        )
        

  
def legend(ax):
    
    ax.legend(
        ncol = 2, 
        bbox_to_anchor = (0.5, 1.3),
        loc = "upper center"
        )



        
def plot_events_infos(ax, row, LIST):
    
    
    
    for col, total in enumerate(LIST):    
        
        pl.plot_infos(
            ax[row, col], 
            total, 
            x = 0.55, y = 0.2,
            translate = True
            )
        
        legend(ax[0, col])
        l = b.chars()[col]
        
        ax[0, col].text(
            -0.1, 1.2, f'({l})', 
            fontsize = 35,
            transform = ax[0, col].transAxes
            )
        
        
def FigureAxes(nrows = 4):
    
    fig, ax = plt.subplots(
          ncols = nrows // 2, 
          nrows = nrows,
          figsize = (20, 14), 
          dpi = 300, 
          sharex = 'col', 
          sharey = 'col'
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.18
        )
    
    return fig, ax 



def plot_distributions_seasons(
        df, 
        parameter = 'gamma',
        limit = 86
        ):
    
    fig, ax = FigureAxes()

    names = ['march', 'june', 'september', 'december']
    
    
    for row, name in enumerate(names):
        
        total_epb = []
        total_day = []
        
        
        df_season = c.SeasonsSplit(df, name)
        
        df_index = c.DisturbedLevels(df_season.sel_season)
        
        F107_labels = df_index.solar_labels(limit)
        
        for index, df_level in enumerate(df_index.F107(limit)):
    
            ds, epb = pl.plot_distribution(
                    ax[row, 0], 
                    df_level, 
                    parameter,
                    label = F107_labels[index]
                    )
            
            total_epb.append(epb)
            
            days = pl.plot_histogram(
                    ax[row, 1], 
                    ds, 
                    index,
                    label = F107_labels[index]
                    )
            
            total_day.append(days)
                    
            ax[row, index].text(
                0.07, 0.82,
                f'{df_season.name}',
                transform = ax[row, index].transAxes
                )
        
        LIST = [total_epb, total_day]
        plot_events_infos(ax, row, LIST)
            
        
    FigureLabels(
        fig, 
        translate = True, 
        fontsize = 30
        )
    
    return fig


def main():


    df = c.concat_results('saa')
    limit = c.limits_on_parts(df['f107a'])
    
    fig = plot_distributions_seasons(
            df, 
            parameter = 'gamma',
            limit = limit
            )
    FigureName = 'seasonal_all_periods'
     
    fig.savefig(
         b.LATEX(FigureName, folder = 'distributions/pt/'),
         dpi = 400
         )