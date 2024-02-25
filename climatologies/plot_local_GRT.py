import matplotlib.pyplot as plt 

def plot_yearly_single_parameters(df):
    
    
    fig, ax = plt.subplots(
        nrows = 4,
        figsize = (10, 12), 
        dpi = 300, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    cols = ['ge', 'L', 'vp', 'gamma2']
    
    names = ['$g / \\nu_{in} ~(m/s)$', 
             '$L^{-1}~(m^{-1})$',
             '$V_p (m/s)$', 
             '$\\gamma_{RT}~(s^{-1})$']
    
    ylim = [[10, 100], [0, 5], [-5, 50], [0, 2]]
    for i, col in enumerate(cols):
        
        ax[i].plot(df[col])
        
        ax[i].set(ylabel = names[i], 
                  ylim = ylim[i])
        