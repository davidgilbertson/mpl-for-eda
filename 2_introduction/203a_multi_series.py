import matplotlib.pyplot as plt

fig, ax = plt.subplots()

ax.plot([1, 2, 3, 2], label="Line one")
ax.plot([2, 3, 4, 3, 7], label="Line two")
ax.legend()

plt.show()
