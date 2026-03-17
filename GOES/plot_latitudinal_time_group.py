import pandas as pd 
import matplotlib.pyplot as plt
import GEO as gg
import datetime as dt 
import GOES as gs 
import base as b 
import numpy as np 

year = 2012
df = b.load(f"GOES/data/nucleos_40/{year}").copy()

df 