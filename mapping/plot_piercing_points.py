import GEO as gg
import matplotlib.pyplot as plt
import datetime as dt 
import plotting as pl
import base as b
import PlasmaBubbles as pb 
import os 
import numpy as np 
import cartopy.crs as ccrs
import GNSS as gs

def plot_ipp_on_map(sel, ticks):
    fig, ax = plt.subplots(
            figsize = (10, 10), 
            dpi = 300, 
            subplot_kw = 
            {'projection': ccrs.PlateCarree()}
            )
    
    dn = sel.index[0]
    # img = ax.scatter(
    #       sel.lon,
    #       sel.lat, 
    #       c = sel.roti, 
    #       s =  20, 
    #       vmin = ticks[0], 
    #       vmax = ticks[-1],
    #       cmap = 'jet'
    #       )
     
    matrix = gs.generate_matrix_tec(
            sel['lat'].values, 
            sel['lon'].values, 
            sel['roti'].values,
            BAD_VALUE = -1
            )

    # matrix = np.where(matrix < 0, np.nan, matrix)
    values = gs.full_binning(matrix, BAD_VALUE = -1)
    
    matrix = np.where(values < 0, np.nan, values)
    
    lon = np.arange(-85, -35, 0.5)
    lat = np.arange(-60, 10, 0.5)
    img = ax.contourf(lon, lat, matrix, 40, cmap = 'jet')
    
    plt.colorbar(img)
    
    gg.map_attrs(
        ax, dn.year, 
        grid = False,
        degress = None
        )


df =  pb.load_filter('206', 
     remove_noise = True
     )
dn = dt.datetime(2022, 7, 25, 3)


delta = dt.timedelta(minutes = 20)
start = df.index[0]
sel = df.loc[start  + delta]
ticks = np.arange(0, 0.5, 0.1)


matrix = gs.generate_matrix_tec(
         sel['lat'].values, 
         sel['lon'].values, 
         sel['roti'].values,
         BAD_VALUE = -1
         )

# plot_ipp_on_map(sel, ticks)

# matrix.min(), matrix.max()

def full_binning(matrix_raw, max_binning = 12, BAD_VALUE =-1):

    n_lon = matrix_raw.shape[1]
    n_lat = matrix_raw.shape[0]
    result_matrix = np.full([n_lat, n_lon], BAD_VALUE)

    current_matrix = matrix_raw

    for n_binning in range(1, max_binning + 1):
        
        for i_lat in range(n_binning, (n_lat - n_binning - 1)):
            
            for i_lon in range(n_binning, (n_lon - n_binning - 1)):

                sub_mat_raw = matrix_raw[
                    (i_lat - n_binning):(i_lat + n_binning),
                    (i_lon - n_binning):(i_lon + n_binning)]
                
                total_valid_tec_raw = (
                    sub_mat_raw != BAD_VALUE).sum()
                
                total = np.nansum(sub_mat_raw)
                print(total_valid_tec_raw)
               
                # if (total_valid_tec_raw > 
                #     0) & (result_matrix[i_lat, i_lon] == BAD_VALUE):
                    
                #     sub_mat = current_matrix[
                #         (i_lat - n_binning):(i_lat + n_binning),
                #         (i_lon - n_binning):(i_lon + n_binning)]
                    
                    
                #     print(sub_mat)
                    # total_sub_mat = sub_mat[sub_mat != BAD_VALUE].sum()
                    # total_valid_tec = (sub_mat != BAD_VALUE).sum()
                    # tec_medio = BAD_VALUE

                    # # if total_valid_tec > 0:
                    # tec_medio = total_sub_mat / total_valid_tec

                    # result_matrix[i_lat, i_lon] = tec_medio

        current_matrix = result_matrix
    

    return result_matrix
values = full_binning(matrix, max_binning = 12, BAD_VALUE = np.nan)
# bins = np.arange(0, 0.2, 0.01)
# plt.hist(values.ravel(), bins = bins )

values.max(), values.min()