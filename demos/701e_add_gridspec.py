import matplotlib.pyplot as plt

import mpl_utils

mpl_utils.setup()
fig = plt.figure(num="GridSpec", clear=True)

gs = fig.add_gridspec(
    nrows=3,
    ncols=2,
    width_ratios=[3, 1],
)

# Longhand
subplot_spec = gs.new_subplotspec(loc=(0, 0), rowspan=2)
ax1 = fig.add_subplot(subplot_spec, facecolor="tab:blue")

# Shorthand
ax2 = fig.add_subplot(gs[1:, 1], facecolor="tab:orange")
ax3 = fig.add_subplot(gs[2, 0], facecolor="tab:green")
