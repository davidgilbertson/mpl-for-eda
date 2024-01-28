import matplotlib.pyplot as plt

import mpl_utils

mpl_utils.setup()
fig = plt.figure(num="subplot2grid", clear=True)

ax1 = plt.subplot2grid(
    shape=(3, 2),
    loc=(0, 0),
    rowspan=2,
    colspan=1,
    title="Axes 1",
    facecolor="tab:blue",
)

ax2 = plt.subplot2grid(
    shape=(3, 2),
    loc=(0, 1),
    rowspan=3,
    colspan=1,
    title="Axes 2",
    facecolor="tab:orange",
)

ax3 = plt.subplot2grid(
    shape=(3, 2),
    loc=(2, 0),
    rowspan=1,
    colspan=1,
    title="Axes 3",
    facecolor="tab:green",
)

ax1.get_gridspec().set_height_ratios([4, 4, 1])
