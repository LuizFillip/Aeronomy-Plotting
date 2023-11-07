# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 22:29:59 2023

@author: Luiz
"""

import numpy as np
import matplotlib.pyplot as plt 
from astropy.timeseries import LombScargle


infile = 'renan.txt'

y = open(infile).read().split()

y = np.array(y, dtype = np.int64)

fig, ax = plt.subplots(
    dpi = 300, 
    figsize = (10, 6),
                   nrows = 2)
ax[0].plot(y)
ax[0].set(ylim = [0, 140])
t = np.arange(len(y))
sp = np.fft.fft(y)

ls = LombScargle(t, y)

frequency, power = ls.autopower(
        samples_per_peak = 100,
        minimum_frequency = 1 / 0.6
        )
    

freq = np.fft.fftfreq(t.shape[-1])
ax[1].plot(freq, sp.real)

# ax[1].plot(1/frequency, power)

ax[1].set(xlim = [-0.1, 0.1])

freq[np.argmax(sp.real)]