import matplotlib.pyplot as plt
import pandas as pd
import magnetometers as mm
from common import load_by_time
import settings as s

def contour_map(df):
    ds = pd.pivot_table(
        df, 
        columns = df.index.date, 
        index = 'time', 
        values = 'F'
        )
    
    fig, ax = plt.subplots(
        figsize = (10, 4)
        )
    img = ax.contourf(
        ds.columns, 
        ds.index,
        ds.values, 
        30,
        cmap = 'rainbow')
    ax.set(ylabel = 'Universal time (UT)')
    s.axes_month_format(ax)
    plt.colorbar(img)
    
infile = 'database/magnetometers/mag2.txt'
df = mm.load_mag()
contour_map(df)
