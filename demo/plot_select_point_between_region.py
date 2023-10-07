
from matplotlib import pyplot as plt
import numpy as np

# line equation of the form ax+by+c = 0 through (x0,y0) and (x1,y1);
# ax+by+c < 0 for points left of the line


N = 500
x = np.random.uniform(0, 2, N)
y = np.random.uniform(0, 2.5, N)

def get_line_eq(x0, x1, y0, y1):
    return y0 - y1, x1 - x0, x0 * y1 - x1 * y0


ar, br, cr = get_line_eq(0.8, 1.8, 1.1, 2.0)
in_red = (y >= 1.1) & (x <= 1.8) & (ar * x + br * y + cr >= 0)

ak, bk, ck = get_line_eq(0.8, 1.4, 1.5, 2.05)
in_black = (y >= 1.5) & (x <= 1.4) & (ak * x + bk * y + ck >= 0)

# plt.scatter(x[in_black], y[in_black], s=5, c='k') # inside the black region
# plt.scatter(x[~in_red], y[~in_red], s=5, c='b') # outside the red region
plt.scatter(x[in_red & ~in_black], y[in_red & ~in_black], s=5, c='r') # inside red but outside black

plt.xlim(0.0, 2.0)
plt.ylim(0.0, 2.5)
plt.plot([0, 0.8], [1.1, 1.1], 'k-', lw=2, c='r')
plt.plot([0, 0.8], [1.5, 1.5], 'k-', lw=2)

plt.plot([1.8, 1.8], [2.0, 2.5], 'k-', lw=2, c='r')
plt.plot([1.4, 1.4], [2.05, 2.5], 'k-', lw=2)

plt.plot([0.8, 1.8], [1.1, 2.0], 'k-', lw=2, c='r')
plt.plot([0.8, 1.4], [1.5, 2.05], 'k-', lw=2)

plt.tight_layout()
plt.show()