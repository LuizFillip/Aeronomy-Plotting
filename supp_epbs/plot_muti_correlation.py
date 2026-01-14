import base as b
import core as c 
import pandas as pd 
import matplotlib.pyplot as plt 


b.sci_format(fontsize = 25)

def plot_cross_all_parameters(df2, cols):
    n = len(cols)
    fig, axes = plt.subplots(
        nrows = n, ncols=n, 
        figsize=(14, 14), 
        dpi=300)
    
    for i, x in enumerate(cols):
        for j, y in enumerate(cols):
            ax = axes[i, j]
            ax.scatter(df2[y], df2[x], alpha=0.5, s=30)
            
            # Apenas rotular o eixo mais à esquerda e inferior
            if j == 0:
                ax.set_ylabel(x)
            else:
                ax.set_yticklabels([])
    
            if i == n - 1:
                ax.set_xlabel(y)
            else:
                ax.set_xticklabels([])
    
            # Adicionar coeficiente de correlação
            if i != j:
                corr = df2[[x, y]].corr().iloc[0, 1]
                ax.set_title(f"r={corr:.2f}", fontsize = 20)
    
    plt.tight_layout()
    plt.show()

# df['divtime'].plot(kind = 'hist')

def get_sum(df):

    # Define a função de agregação: 'occ' com soma, o resto com média
    agg_funcs = {col: 'sum' for col in df.columns if col != 'occ'}
    agg_funcs['occ'] = 'sum'
    
    # Agrupa por mês e aplica agregações
    return df.groupby(df.index.month).agg('sum')

def get_avg(df):
    
    agg_funcs = {col: 'mean' for col in df.columns if col != 'occ'}
    agg_funcs['occ'] = 'sum'
    
    return df.groupby(df.index.month).agg(agg_funcs)

# df1 = get_avg(df)


df = c.events_in_storm()

def plot_multi_correlation(df):
    df['occ'] = 1
    
    cols = ['occ', 'bz', 'speed', 'ae',
            'sym', 'f10.7', 'by']
    df = df[cols]
    
    df2 = get_avg(df)  
    
    fig, ax = plt.subplots(
        ncols = 3, 
        nrows = 2,
        figsize = (14, 10),
        sharey= True,
        dpi = 300
        )
    
    plt.subplots_adjust(
        wspace = 0.1,
        hspace = 0.3
        )
    
    for i, ax in enumerate(ax.flat):
        y = 'occ'
        x = cols[1:][i]
        ax.scatter( df2[x], df2[y], color = 'k', s = 100)
        corr = df2[[x, y]].corr().iloc[0, 1]
        
        ax.text(
            0.05, 0.85, f"r={corr:.2f}", 
            transform = ax.transAxes, 
            fontsize = 25
            )
        
        ax.set(xlabel = x)
        
        if  i == 0 or i == 3:
            
            ax.set(ylabel = 'Number of cases', ylim = [0, 15])
            
    return fig 


df 
            