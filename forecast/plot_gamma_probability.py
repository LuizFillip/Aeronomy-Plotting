import matplotlib.pyplot as plt 
import core as c 
import base as b 

b.config_labels()



def plot_gamma_predict_epbs(obs, pred):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 3,
        sharex=True,
        figsize = (12, 10)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    ax[0].plot(obs['gamma'])
    
    ax[1].plot(pred *100, color = 'k')
    
    ax[2].plot(obs['epb'], color = 'k')
    
    ax[1].set(
        ylabel = 'Probability (\%)', 
        ylim = [-20, 120], 
        yticks = list(range(0, 125, 25))
        )
  
    ax[0].set(
        ylabel = '$\gamma_{RT}$', 
        yticks = list(range(0, 4, 1))
        )
    
    ax[2].set(
        ylabel = 'EPB observed', 
        ylim = [-0.2, 1.2], 
        yticks = [0, 1]
        )
    b.format_month_axes(ax[2])
    
    for line in [0, 1]:
        
        ax[1].axhline(line * 100, lw = 0.5, linestyle = '--') 
        ax[2].axhline(line, lw = 0.5, linestyle = '--')

parameter = 'gamma'

df = c.load_results('saa', eyear = 2023)
obs = df.loc[df.index.year == 2023, ['gamma', 'epb']]
pred = c.forecast_epbs(
    year_threshold = 2023, 
    parameter= 'gamma')
pred = pred.data['predict']

plot_gamma_predict_epbs(obs, pred)