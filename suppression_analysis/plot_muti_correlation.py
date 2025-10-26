import base as b
import core as c 
import pandas as pd 
import matplotlib.pyplot as plt 

df = b.load('core/src/geomag/data/stormsphase')

df = c.geomagnetic_analysis(df)

df = df.loc[df.sym > -30]

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

 
df['occ'] = 1


cols = ['occ', 'bz', 'speed', 'ae', 'sym']
df = df[cols]

# Substitua por sua função que agrega (por exemplo, soma mensal)
df2 = get_sum(df)  # Ex: df.resample('M').sum()

def plot_cross_all_parameters():
    n = len(cols)
    fig, axes = plt.subplots(nrows=n, ncols=n, figsize=(18, 18), dpi=300)
    
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
                ax.set_title(f"r={corr:.2f}", fontsize=20)
    
    plt.tight_layout()
    plt.show()
