import matplotlib.pyplot as plt
import numpy as np

import mpl_utils

mpl_utils.setup()
fig, axs = plt.subplots(
    nrows=2,
    ncols=2,
    height_ratios=[100, 9],
    width_ratios=[2, 1],
    num="subplots",
    clear=True,
)

for pos, ax in np.ndenumerate(axs):
    ax.set_title(f"Axes {pos}")
    ax.set_facecolor("tab:blue")

# The GridSpec behind the scenes
grid_spec = axs[0, 0].get_gridspec()
