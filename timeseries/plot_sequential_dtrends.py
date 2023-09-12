
import os.path
import sys


file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from Intermagnet import *



def SequentialPlot(files, infile, figsize = (6, 10), save = False,
                   component = 'H', N = 10, fontsize = 13):
    
    nrows = len(files)
    files = files[::-1]
    
    fig, axs = plt.subplots(figsize = figsize, 
                           sharex = True, 
                           nrows = nrows)
    
    plt.subplots_adjust(hspace = 0)
    
    
    for num, ax in enumerate(axs.flat):
        
        instance_ = intermagnet(files[num], infile)
        
        df = instance_.dataframe(component = component)
        
        df['dtrend'].plot(ax = ax, color = 'k', lw = 1)
        
        # Plot Subract from running average 
     
    
        # Setting limits
        ax.set(xlabel = 'Universal time (UT)',
               xlim = [df.index[0], df.index[-1]])
        
    
        #Put the name of location
        ax.text(0.03, 0.8, instance_.name, transform = ax.transAxes)
        
    
        if num == 0:    
            ax.spines['bottom'].set_visible(False)       
        elif num == (nrows - 1):    
            ax.spines['top'].set_visible(False)
        else:
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
        
        if instance_.name == 'Hornsund':
            ax.set(ylim = [-50, 50])
        
        #ax.axvspan(tm1, tm2, color='lightgrey', alpha=0.4, lw=0)
        
        # Setting hour locator (must be in datetime format) on the xaxis 
        ax.xaxis.set_major_formatter(dates.DateFormatter('%H'))
        ax.xaxis.set_major_locator(dates.HourLocator(interval = 2))
        
    

    if component == ('H'):
        ylabel = 'Horizontal'
    elif component == 'Z':
        ylabel = 'Vertical'
    elif component == 'F':
        ylabel = 'Total'
        
    # Datetime format
    def date(format_ = "%d/%m/%Y"):
        return instance_.date.strftime(format_)
    
    fig.text(0.01, 0.5, f'{ylabel} component (nT)', va='center', 
                 rotation='vertical', fontsize = fontsize)   
    
    fig.suptitle(f'INTERMAGNET Magnetometers Network\n dTrend - {date()}', 
             y = 0.93, fontsize = fontsize)
    
    plt.rcParams.update({'font.size': fontsize}) 
    
    if save:
          
        NameToSave = f'{ylabel}{date(format_ = "%d%m%Y")}dTrendAnalysis.png'
        print(NameToSave)
        path_to_save = 'Figures/INTERMAGNET/'
    
        plt.savefig(path_to_save + NameToSave, 
                    dpi = 100, bbox_inches="tight")
        
infile = 'Database/Intermag/'

# Get filenames from acromicos list (as latitudes and longitudes)
# I must fix somethings in this routine, yet
files = get_filenames_from_codes(infile)


SequentialPlot(files, infile, save = True)