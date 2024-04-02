# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 09:08:04 2024

@author: Luiz
"""

import matplotlib.pyplot as plt
from skimage import io

from skimage import data
from skimage import color, morphology

image =  io.imread('renan1.jpg', as_gray = True)
# image = color.rgb2gray(img)#[:500, :500]

# footprint = morphology.disk(7)
# res = morphology.white_tophat(image, footprint)

# fig, ax = plt.subplots(ncols=3, figsize=(20, 8))
# ax[0].set_title('Original')
# ax[0].imshow(image, cmap='gray')
# ax[1].set_title('White tophat')
# ax[1].imshow(res, cmap='gray')
# ax[2].set_title('Complementary')
# ax[2].imshow(image - res, cmap='gray')

# plt.show()

import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import convolve2d as conv2

from skimage import color, data, restoration

rng = np.random.default_rng()

# astro = color.rgb2gray(data.astronaut())
astro= io.imread('renan1.jpg', as_gray = True)
psf = np.ones((5, 5)) / 20
astro = conv2(astro, psf, 'same')
# Add Noise to Image
astro_noisy = astro.copy()
astro_noisy += (rng.poisson(lam=25, size=astro.shape) - 20) / 255.

# Restore Image using Richardson-Lucy algorithm
deconvolved_RL = restoration.richardson_lucy(astro_noisy, psf, num_iter=30)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(8, 5))
plt.gray()

for a in (ax[0], ax[1], ax[2]):
       a.axis('off')

ax[0].imshow(astro)
ax[0].set_title('Original Data')

ax[1].imshow(astro_noisy)
ax[1].set_title('Noisy data')

ax[2].imshow(deconvolved_RL, vmin=astro_noisy.min(), vmax=astro_noisy.max())
ax[2].set_title('Restoration using\nRichardson-Lucy')


fig.subplots_adjust(wspace=0.02, hspace=0.2,
                    top=0.9, bottom=0.05, left=0, right=1)
plt.show()