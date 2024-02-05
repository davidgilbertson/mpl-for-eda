import matplotlib.pyplot as plt

import mpl_utils

mpl_utils.setup()
fig = plt.figure(num="add_subplot", clear=True)

# single-number API rows-cols-index
# ax1 = fig.add_subplot(221, title="Axes 1")
# ax2 = fig.add_subplot(222, title="Axes 2")
# ax3 = fig.add_subplot(223, title="Axes 3")

# You can't define height/width ratios, but axes can span multiple grid cells
ax1 = fig.add_subplot(5, 5, (1, 17), title="Axes 1")
ax2 = fig.add_subplot(5, 5, (3, 20), title="Axes 2")
ax3 = fig.add_subplot(5, 5, (21, 24), title="Axes 3")

for i in range(25):
    row, col = divmod(i, 5)
    fig.text(
        s=i + 1,
        x=(col / 5) + (1 / 10),
        y=1 - ((row / 5) + (1 / 10)),
        fontdict=dict(size=40),
        ha="center",
        va="center",
    )


# You can still loop over axes in fig.axes
for ax in fig.axes:
    ax.set_facecolor("tab:blue")

subplot_spec = ax2.get_subplotspec()
