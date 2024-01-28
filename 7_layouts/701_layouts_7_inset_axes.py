import matplotlib.pyplot as plt
from matplotlib.transforms import IdentityTransform
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import mpl_utils

mpl_utils.setup()
fig, ax1 = plt.subplots(num="inset_axes", clear=True)

ax1.set_facecolor("tab:blue")

ax2 = ax1.inset_axes(
    bounds=(1.05, 0, 0.2, 1),
    facecolor="tab:orange",
)
ax2.set(xticks=[], yticks=[])

# Using pixels for x/y/width/height
ax3 = ax1.inset_axes(
    bounds=(100, 100, 400, 100),  # pixels
    transform=IdentityTransform(),
    facecolor="tab:green",
)
ax3.set(xticks=[], yticks=[])

# A different inset axes, uses AnchoredOffsetbox behind the scenes
# This will not be a child of ax1 like the others
ax4 = inset_axes(
    ax1,
    loc="lower left",
    bbox_to_anchor=(200, 300),  # pixels
    width=2,  # hectopixels
    height=3,  # hectopixels
)
ax4.set_facecolor("tab:red")
ax4.set(xticks=[], yticks=[])
