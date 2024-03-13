import core as c 
import matplotlib.pyplot as plt 
import base as b

b.config_labels()



def plot_seasonal_gamma_vs_pre(df, col = 'gamma'):

    fig, ax = plt.subplots(
        sharey= 'row', 
        figsize = (12, 10),
        dpi = 300,
        sharex = 'col',
        nrows = 2, 
        ncols = 2
        )
    
    plt.subplots_adjust(wspace = 0.05)
    
    if col == 'gamma':
        gamma_eq = '$\\gamma_{RT} = (V_P - U_L^P + \\frac{g_e}{\\nu_{in}^{eff}})K^F$'
    else:
        gamma_eq = '$\\gamma_{RT} = (\\frac{g_e}{\\nu_{in}^{eff}})K^F$'
    
    names = ['march', 'june', 'september', 'december']
    
    
    for i, ax in enumerate(ax.flat):
        
        name = names[i]
        
        ds_split = c.SeasonsSplit(df, name)
        
        ds = ds_split.sel_season
        
        x, y = ds['vp'].values, ds[col].values
        
        fit = b.linear_fit(x, y)
        r2 = fit.r2_score
        ax.scatter(x, y, s = 10, c = 'k')
        
        ax.plot(x, fit.y_pred, lw = 2, color = 'red')
        ax.text(
            0.1, 0.8, f'$R^2$ = {r2}', 
            transform = ax.transAxes)
        
        ax.set(title = ds_split.name)
    
    fig.suptitle(gamma_eq)
    fontsize = 30
    fig.text(
         0.04, 0.37, 
         b.y_label('gamma'), 
         fontsize = fontsize, 
         rotation = 'vertical'
         )
     
    fig.text(
         0.45, 0.05, 
         b.y_label('vp'), 
         fontsize = fontsize
         )
    
    return fig  

df = c.concat_results('saa')


def plot_general_correlation(df, ax = None, col = 'gamma'):
    
    
    if ax is None:
        fig, ax = plt.subplots(dpi = 300)
        ax.set(ylabel = b.y_label('gamma'), 
               xlabel = b.y_label('vp'))
    
    
    x, y = df['vp'].values, df[col].values
    
    fit = b.linear_fit(x, y)
    r2 = fit.r2_score
    ax.scatter(x, y, s = 10, c = 'k')
    
    ax.plot(x, fit.y_pred, lw = 2, color = 'red')
    ax.text(
        0.1, 0.8, f'$R^2$ = {r2}', 
        transform = ax.transAxes)
    
       
    return fig


# fig = plot_general_correlation(df, col = 'gravity')

fig = plot_seasonal_gamma_vs_pre(df, col = 'gravity')
