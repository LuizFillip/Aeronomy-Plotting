import PlasmaBubbles as pb 
import matplotlib.pyplot as plt 
def plot(ip, ds, df):
    

    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 3, 
        sharex = True, 
        figsize = (10, 6)
        )
    
    ax[0].plot(ip['f107'])
    ax[0].set(ylim = [50, 250])
    ax[1].plot(ds[['mean', 'base', 'std']])
    
    values = pb.set_value(ds['mean'], 
                       ip['f107a'], 
                       ds['base']).dropna()
    ax[2].plot(values)
    
    mvals = values.resample('1M').asfreq()
    
    ax[2].plot(mvals)
    
    ax[1].set(xlim = [df.index[0], df.index[-1]])
