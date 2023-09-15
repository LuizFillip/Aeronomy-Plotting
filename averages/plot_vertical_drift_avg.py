# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 22:33:12 2023

@author: Luiz
"""

import base as b 
import matplotlib.pyplot as plt 
import events as ev  


df = b.load('all_results.txt')

l, m, h = ev.solar_flux_cycles(df)

l['vp']
