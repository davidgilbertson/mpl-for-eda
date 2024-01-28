import matplotlib.pyplot as plt

import mpl_utils

mpl_utils.setup()

fig, ax1 = plt.subplots(num="add_axes", clear=True)
ax1.set(facecolor="tab:blue")

ax2 = fig.add_axes((0.4, 0.2, 0.8, 0.3), facecolor="tab:orange")

# plt.axes() will call gcf().add_axes() when an arg is passed
ax3 = plt.axes((0.3, 0.6, 0.8, 0.3), facecolor="tab:green")
