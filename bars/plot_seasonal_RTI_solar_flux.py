import core as c
import base as b 
import matplotlib.pyplot as plt
import numpy as np


df = c.concat_results('saa')


ranges = np.arange(0, 4, 0.8)  

def count_occurrences_in_range(
        df, col_name,lower, upper):
    
    return df[(df[col_name] >= lower) & 
              (df[col_name] < upper)].shape[0]


def occurrences_by_range():
    
    out = {}
   

    for i in range(len(ranges) - 1):
    
        lower, upper = (ranges[i], ranges[i + 1])
        occurrences = count_occurrences_in_range(
            df, 'gamma', lower, upper)
        out[lower] = occurrences
        
    return out