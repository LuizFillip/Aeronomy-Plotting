import base as b 
import matplotlib.pyplot as plt 
import events as ev  
import numpy as np 



infile = 'digisonde/data/PRE/saa/2013_2022.txt'
infile = 'digisonde/data/drift/PRE/saa/2021.txt'

infile = "D:\\drift\\2013.txt"
df = b.load(infile)


df['filt'].plot()