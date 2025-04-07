import matplotlib.pyplot as plt
import datetime as dt 
import numpy as np 
import digisonde as dg 
import base as b 
import plotting as pl


 
 # df = df.between_time('17:00', '21:00')
 
 # for x in df.columns:
 #     vls = b.filter_frequencies(
 #             df[x], 
 #             high_period = 5, 
 #             low_period = 1, 
 #             fs = 6, 
 #             order = 1
 #             )
 #     print(len(vls), len(df))
 #     ax[i].plot(df.index, vls)