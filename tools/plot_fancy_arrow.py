# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 12:22:20 2024

@author: Luiz
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


fig = plt.figure()
ax1 = fig.add_subplot(121)

ax1.set_xlim(-50,150)
ax1.set_ylim(-60,165)

style="Simple,tail_width=0.5,head_width=4,head_length=8"
kw = dict(arrowstyle=style)
a1 = FancyArrowPatch((0, 0), (99, 100),connectionstyle="arc3,rad=-0.3", **kw)

ax1.add_patch(a1)