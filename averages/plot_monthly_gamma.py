import base as b
import core as c
import numpy as np


df = c.load_results("saa", eyear=2022)

ds = df.resample("1M").mean()
bins = np.arange(0, 3, 0.01)
df["gamma"].plot(kind="hist", bins=bins)
