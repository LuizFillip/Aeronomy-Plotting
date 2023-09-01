import matplotlib.pyplot as plt
from base import load



fig, ax = plt.subplots(
    figsize = (12, 5)
    )
df = load('roti_test.txt')

df['-40'].plot()