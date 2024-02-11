import matplotlib.pyplot as plt

import mpl_utils

mpl_utils.setup()
fig, axs = plt.subplot_mosaic(
    mosaic=[
        ["Top left", "Top right"],
        ["Bottom row", "Bottom row"],
    ],
    per_subplot_kw={
        "Top left": dict(facecolor="tab:blue"),
        "Top right": dict(facecolor="tab:orange"),
        "Bottom row": dict(facecolor="tab:green"),
    },
    height_ratios=[100, 8],
    width_ratios=[2, 1],
    num="subplot_mosaic",
    clear=True,
)

axs["Top left"].set_title("Top left")
axs["Top right"].set_title("Top right")
axs["Bottom row"].set_title("Bottom row")
