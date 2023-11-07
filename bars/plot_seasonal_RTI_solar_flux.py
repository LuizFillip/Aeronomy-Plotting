import events as ev 
import base as b 
import matplotlib.pyplot as plt
import numpy as np


df = ev.concat_results('saa')


ranges = np.arange(0, 4, 0.8)  

def count_occurrences_in_range(
        df, col_name,lower, upper):
    
    return df[(df[col_name] >= lower) & 
              (df[col_name] < upper)].shape[0]


occurrences_by_range = {}
   



for i in range(len(ranges) - 1):

    lower, upper = (ranges[i], ranges[i + 1])
    occurrences = count_occurrences_in_range(
        df, 'gamma', lower, upper)
    occurrences_by_range[lower] = occurrences
    
occurrences_by_range