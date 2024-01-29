import matplotlib.pyplot as plt

plt.rcParams["backend"] = "TkAgg"
plt.ion()

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 2, 3])
