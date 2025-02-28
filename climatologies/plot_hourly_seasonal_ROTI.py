import numpy as np 
import matplotlib.pyplot as plt 
import base as b 
import pandas as pd 
import datetime as dt

b.config_labels()

out = []
for year in range(2013, 2023):
    
    infile = f'database/epbs/longs/{year}'
    
    df = b.load(infile)
    
    df.loc[df.between_time('23:58', '00:02').index, :] = np.nan
    
    df = df.interpolate()
    df['time'] = b.time2float(df.index)
    
    df['date'] = df.index.date
    
    out.append(df)


ds = pd.pivot_table(
    pd.concat(out), 
    columns = 'date', 
    index = 'time', 
    values = '-50'
    )

#%%%%

def interpolate_matrix(matrix):
    if isinstance(matrix, (list, np.ndarray)):  # Garante que é uma matriz
        matrix = np.array(matrix, dtype=np.float64)  # Converte para array
        mask = np.isnan(matrix)
        if np.any(mask):  # Só interpola se houver NaN
            x = np.arange(len(matrix))
            matrix[mask] = np.interp(x[mask], x[~mask], matrix[~mask])  # Interpolação linear
        return matrix
    return matrix

# Aplicar a interpolação em cada célula
# ds = ds.applymap(interpolate_matrix)
# ds = ds.replace(np.nan, 0)
# ds = ds.interpolate()
fig, ax = plt.subplots(
    figsize = (16, 8), 
    dpi = 300)

ax.contourf(
    ds.columns, 
    ds.index, 
    ds.values,
    30, 
    # cmal = 
    )


# dn = dt.datetime(2013, 1, 1, 20)
# df1 = b.sel_times(df, dn, hours = 12)

#%%
# df1 = df1.interpolate()



# df1['-50'].plot()