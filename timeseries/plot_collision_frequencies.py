import matplotlib.pyplot as plt
import ionosphere as io
import pandas as pd

infile = 'database/MSIS/sites/car.txt'
infile = "fp_temp.txt"
infile = "nui_temp.txt"
df = pd.read_csv(infile, index_col=0)
df.index = pd.to_datetime(df.index)
    

df['nui'].plot()
df['avg'].plot()