import matplotlib.pyplot as plt
import GNSS as gs 
import PlasmaBubbles as pb  
import os

path = gs.paths(2019, 1, root = os.getcwd())
  
df = pb.load_filter(path.fn_roti, factor = 4)
 
# plot_roti_avg(ax, df)

fig, ax = plt.subplots()
 
day = df.between_time(
 '12:00', '20:00'
 )
 

avg_day = day['roti'].mean()
 # ax.axhline(avg_day)



ax.axhline(y=avg_day, xmin=0.5, xmax=0.83, color='g', linestyle='-')

# Set the y-axis limits to focus on the interval
plt.ylim(0, 1)
plt.xlim(0, 24)

# Display the plot
plt.show()
