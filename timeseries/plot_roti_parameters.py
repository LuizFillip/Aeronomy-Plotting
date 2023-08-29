import matplotlib.pyplot as plt
import GNSS as gs
import base as b
import datetime as dt

b.config_labels()

def plot_roti_parameters(
        path, 
        station = 'amte', 
        prn = 'E18'):
    
    ds = b.load(path.fn_roti)

    ds = ds[(ds['sts'] ==  station)] 

    fig, ax = plt.subplots(
        figsize = (10, 8),
        nrows = 3,
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    
    roti  = ds.loc[
        (ds['prn'] == prn), 'roti'].dropna()
    
    tec = b.load(
        path.fn_tec(station))[prn].dropna()
    
    ax[0].plot(tec)
    ax[0].set(ylabel = "STEC (TECU)", title = f'{station} -{prn}')
    
    ax[2].scatter(roti.index, roti, s = 1)

    ax[2].set(
              ylim = [0, 6], 
              ylabel = "ROTI")

    ax[2].axhline(1, color = 'r')

    
    
    time_out, rot = gs.rot(tec, tec.index)
    ax[1].plot(time_out, rot)
    ax[1].axhline(0, color = 'r')
    ax[1].set(ylabel = "ROT")
    
    
    
    b.format_time_axes(ax[2], hour_locator = 3)
    
    return ax
    

    

# plot_roti_parameters(station, prn, tec)



def roti_by_station(ds):
    
    for station in ds['sts'].unique():
        fig, ax = plt.subplots()
        sel_sts = ds.loc[ds['sts'] ==  station]
        
        for prn in sel_sts['prn'].unique():
            sel_sts.loc[
                sel_sts['prn'] == prn, 
                        'roti'].plot(ax = ax)
            ax.set(title = station, ylim = [0, 5])
        



def all_prns_by_station(ds,  station = 'pasm'):
     
    sel_sts = ds.loc[ds['sts'] ==  station]
    
    for prn in sel_sts['prn'].unique():
        plot_roti_parameters(
                path, 
                station = station, 
                prn = prn
                )

year = 2021
doy = gs.doy_from_date(dt.date(year, 7, 7))
path = gs.paths(year, doy)
ds = b.load(path.fn_roti)


# ds = gs.filter_bad_prns(ds, path)


# # # 
# ds[ds['roti'] > 1]

# # 
# df = ds.loc[(ds['sts'] == 'amua') &
#             (ds['prn'] == 'R20') &
#             (ds['roti'] > 1)]


# # df = ds.loc[(ds['sts'] == 'apma') &
# #             (ds['prn'] == 'G05')]

plot_roti_parameters(
        path, 
        station = 'apma', 
        prn = 'G29'
        )
# fig, ax = plt.subplots()
# df['roti'].plot(ax = ax)
# import numpy as np
# avg = np.gradient(df['roti'])
# ax.plot(df.index, avg)


# doy 