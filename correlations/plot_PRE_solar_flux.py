import matplotlib.pyplot as plt
import base as b 

filename = 'all_results.txt'


df = b.load(filename)

# df = df[(df['kp_max'] <= 4) &
#         (df['vp'] < 60)]

# plt.scatter(
#     df['f107'],
#     df['vp']
#     )


df['vp'].plot()