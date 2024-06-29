import matplotlib.pyplot as plt 
import base as b 

def plot_seasonal_Kp(df):
    
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (12, 6)
        )
    
    df['kp'].plot(kind = 'bar', 
                  ax = ax, 
                  color =  'gray',
                  legend = False,
                  edgecolor = 'k')
    
    translate = False 
    
    s_year = 2013
    e_year = 2023
    
    if translate:
        ylabel = 'Kp$_{avg} - Kp_{min}$'
        xlabel = 'Anos'
        sector = 'Setor'
        title =  + f'({s_year} - {e_year})'
        language = 'pt'
    else:
        ylabel ='$\\bar{Kp} - \\bar{Kp}_{min}$'
        xlabel = 'Months'
        sector = 'Sector'
        title =  f'{s_year} - {e_year}'
        language = 'en'
    
    ax.set(
      title = title,
        ylabel = ylabel,
        xlabel = xlabel,
        xticklabels = b.month_names(
            sort = True, language = language),
        # ylim = [0, 1]
        )
    
    plt.xticks(rotation = 0)
    
    return fig 