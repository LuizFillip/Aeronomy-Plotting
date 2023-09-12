import PlasmaBubbles as pb
import matplotlib.pyplot as plt 
import numpy as np 
import base as b 
import datetime as dt 



year = 2013

df = pb.concat_files(year)

dn = dt.datetime(year, 1, 1, 20)

df = b.sel_times(df, dn, hours = 11)
