import matplotlib.pyplot as plt
import datetime as dt
from common import load
from events import storms_types
from utils import linear_fit


def join_data():
    infile = "database/Digisonde/vzp/saa/2014_2015_2.txt"
    mod = load(infile)['vp'].to_frame('iono')
    b = 'database/Results/joined/vp_epbs.txt'

    obs = load(b)[['vp', 'kp']]
    
    return mod.join(obs).dropna()


def plot_corr_drift_iono():
    
    fig, ax = plt.subplots(
        figsize = (7, 5), 
        sharex = True, 
        sharey = True
        )      

    ds = join_data()
    
    
    ds['rate'] = abs(1 - ds['iono'] / ds['vp'])
    
    ds = ds.loc[ds['rate'] < 0.3]
    x, y = ds['iono'].values, ds['vp'].values
    ax.scatter(x, y)
    
    r2, yp = linear_fit(x, y)
    
    ax.plot(x, yp, 
            label = f'$R^2$ = {r2}', 
            color = 'r')
    
    ax.set(xlabel = 'Data reduced (SAO-Explorer)',
           ylabel = 'Doppler measurement (DRIFT-X)', 
           xlim = [-10, 90], 
           ylim = [-10, 90])
    
    ax.legend()
    # plt.show()
    
    print(ds)
    
    
plot_corr_drift_iono()

