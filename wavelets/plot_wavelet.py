# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 10:23:32 2022

@author: LuizF
"""
import os.path
import sys
import matplotlib.ticker as ticker
import matplotlib as mpl
from pylab import *

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

#from MagnetometersAnalysis import *
from Intermagnet import *


def Wavelet(df, ax = None, 
                 transform = 'power', 
                 maximum_period = 1.1, 
                 minimum_period = 0.1):
    
    '''
    Compute and plot wavelet analysis
    software from Torrence and Compo 1998. 
    
    '''
    
    wavelet_path = 'C:\\Users\\LuizF\\Google Drive\\My Drive\\'\
    'Python\\code-master\\wavelets-master\\wave_python\\'
    
    sys.path.insert(1, wavelet_path)
    from waveletFunctions import wave_signif, wavelet
    
    dt = 0.016 # sampling time (1 minute)
    sst = df['dtrend'].values
    time = df['time'].values
    pad = 1
    variance = np.std(sst, ddof=1) ** 2
    mother = 'MORLET'
    lag1 = 0.01
    s0 = 2 * dt  
    
    n  = len(sst)
    if 0:
        variance = 1.0
        sst = sst / np.std(sst, ddof=1)
     
    #wavelet transform
    wave, period, scale, coi = wavelet(sst, dt = dt, pad = pad, s0 = s0)
    
    transform = transform.lower()
    
    # Chooice between
    if transform == 'power':
        # Compute the power spectrum
        power = (np.abs(wave))**2  
        
    elif transform == 'phase':
        # Compute the phase
        power = np.arctan2(np.imag(wave), np.real(wave)) 
    else:
        # Compute the amplitude
        power = np.real(wave)
        
    # Filter the periods
    condition = ((period >= minimum_period) & (period <= maximum_period))
        
    ind = np.where(condition)
    new_period = period[condition]
    new_power = power[ind, :][0]
    new_power = new_power / np.max(new_power)
 
    time = df.index

    
    if ax:
    
        levels = MaxNLocator(nbins=80).tick_values(new_power.min(), 
                                                   new_power.max())
        
        im = ax.contourf(time, new_period, new_power, 
                         levels = levels, cmap = 'jet')
        return im
    
    return time, new_period, new_power, new_sig95

        
def plot(files, infile, nrows = 4, ncols = 2, transform = 'power', 
         component = 'H', fontsize = 14, save = False):
    
    fig, ax = plt.subplots(figsize = (12, 10), 
                           sharex = True, sharey = True,
                           nrows = nrows, ncols = ncols)
    
    plt.subplots_adjust(hspace = 0, wspace = 0)
    
    
    for x in range(nrows):
        for y in range(ncols):
            
            num = ((x + 1) * (y + 1)) - 1
            
    
            filename = files[num]
            
            # Read the files
            instance_ = intermagnet(filename, infile)
            
            df = instance_.dataframe(component = component)
            
           
            im = Wavelet(df, ax[x, y], transform = transform)
            
 
            ax[x, y].text(0.03, 0.89, instance_.name, 
                          transform = ax[x, y].transAxes)
            
            deltatime = datetime.timedelta(minutes = 30)
            
            ax[x, y].set(ylim = [0, 1.3], 
                        xlim = [df.index[0] - deltatime, 
                                df.index[-1] + deltatime],
                         yticks = np.arange(0, 1.2, 0.2))
            
            ax[x, y].xaxis.set_major_formatter(dates.DateFormatter('%H'))   
            ax[x, y].xaxis.set_major_locator(dates.HourLocator(interval = 2))
            
            if y == 0:
                ax[x, y].spines['right'].set_visible(False)
                if x == 0: 
                    ax[x, y].spines['bottom'].set_visible(False)
                elif x == (nrows - 1):
                    ax[x, y].spines['top'].set_visible(False)   
                else:
                    ax[x, y].spines['top'].set_visible(False)   
                    ax[x, y].spines['bottom'].set_visible(False)  
                    
            else:
                ax[x, y].spines['left'].set_visible(False)
                if x == 0: 
                    ax[x, y].spines['bottom'].set_visible(False)
                    ax[x, y].axes.yaxis.set_visible(False)
                elif x == (nrows - 1):
                    ax[x, y].spines['top'].set_visible(False)   
                    ax[x, y].axes.yaxis.set_visible(False)
                else:
                    ax[x, y].spines['top'].set_visible(False)   
                    ax[x, y].spines['bottom'].set_visible(False)  
                    ax[x, y].axes.yaxis.set_visible(False)
 
    cax, kw = mpl.colorbar.make_axes([axes for axes in ax.flat])
    
    if transform == 'power':    
        vmin, vmax, step = 0, 1, 0.1
    else:
        vmin, vmax, step = -1, 1, 0.1
        
    cbar = fig.colorbar(im, cax=cax, **kw, 
                        ticks = np.arange(vmin, vmax + step, step))
    
    cbar.set_label(f'{transform.title()} Spectral Density (normalized)')
    
    fig.text(0.07, 0.5, 'Period (hours)', va='center', 
                 rotation='vertical', fontsize = fontsize)   
    
    fig.text(0.4, 0.08, 'Universal time (UT)', va='center', 
                 rotation='horizontal', fontsize = fontsize) 
    
    # Datetime format
    def date(format_ = "%d/%m/%Y"):
        return instance_.date.strftime(format_)
    
    fig.suptitle(f'Wavelet Analysis - {transform.title()} Spectral - {date()}', 
                 y = 0.9, fontsize = fontsize)
    
    plt.rcParams.update({'font.size': fontsize})    
    
    
    
    if save:
          
        NameToSave = f'{transform.title()}WaveletAnalysis{date(format_ = "%d%m%Y")}.png'
        
        path_to_save = 'Figures/INTERMAGNET/'
    
        plt.savefig(path_to_save + NameToSave, 
                    dpi = 100, bbox_inches="tight")
    
    
    plt.show()            

### Run
#infile = 'Database/Intermag/'

#files = get_filenames_from_codes(infile)

#(files, infile, fontsize = 14, save = True)