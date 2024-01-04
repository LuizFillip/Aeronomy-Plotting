import matplotlib.pyplot as plt
import core as c 
import base as b 


def plot_roti():
    
    return 

def plot_gamma_and_roti(ax, ds):
    
    start = ds.index[0]
    
    df = c.load_raw_roti(start)
    
    df['-50'].plot(ax = ax)
    
    # df2 = c.load_base_gamma(ds)
    
    # ax1 = ax.twinx()
    
    # df2['gamma'].plot(
    #     ax = ax1, 
    #     color = 'b', 
    #     lw = 2, 
    #     ylim = [0, 3]
    #     )
    
    dn = ds.index[0].strftime('%B, %Y')
    
    ax.text(0.01, 0.8, dn,
            transform = ax.transAxes)
    
    ax.set(ylim = [0, 3])
    
    b.format_days_axes(ax)
    
    # ax.set(ylabel = 'ROTI (TECU/min)')
    # ax1.set(ylabel = '$\\gamma_{RT} ~(s^{-1})$')


df = c.concat_results('saa')

 
fig, ax = plt.subplots(
    dpi = 300, 
    nrows = 3, 
    figsize = (12, 8), 
    sharey = True)

b.config_labels()


for ds in c.atypical_occurrences(df, days = 4):
    start = ds.index[0]
    
    df = c.load_raw_roti(start)
    

# for i in range(3):
    
#     plot_gamma_and_roti(ax[i], ds[i]) 