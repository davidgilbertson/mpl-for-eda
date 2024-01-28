import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import mpl_utils

mpl_utils.setup()
fig, ax1 = plt.subplots(num="Divider", clear=True)

ax1.set_facecolor("tab:blue")

# Create a 'divider', allowing us to attach a new axes to ax1
ax_divider = make_axes_locatable(ax1)

# Add a new axes at the bottom
ax2 = ax_divider.append_axes(
    "bottom",
    size=1,  # 1 inch @ 100 dpi, or 100px high
    pad=0.4,  # 40 px
)

ax2.set_facecolor("tab:orange")
# Remove ticks so we can check the exact size
ax2.set(xticks=[], yticks=[])

# Add another to the right, using percent size
ax3 = ax_divider.append_axes("right", size="30%", pad=0.5)
ax3.set_facecolor("tab:green")
