import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(
    nrows=2,
    ncols=1,
    layout="constrained",
)

ax1.plot([1, 2, 3, 2])
ax1.set(title="Line one")

ax2.plot([2, 3, 4, 3, 7])
ax2.set_title("Line two")

plt.show()
