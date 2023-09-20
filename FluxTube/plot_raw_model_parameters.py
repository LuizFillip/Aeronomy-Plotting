import pandas as pd
import matplotlib.pyplot as plt


file = 'FluxTube/data/raw/201502012000.txt'


df = pd.read_csv(file, index_col = 0)

df = df.loc[df['apex'] == 300]

fig, ax = plt.subplots(
    ncols = 3,
    figsize = (12, 5), 
    dpi = 300
    )

deps = ['alt', 'glat', 'glon']

for i, ax in enumerate(ax.flat):
    ax.plot(df['U'], df[deps[i]])