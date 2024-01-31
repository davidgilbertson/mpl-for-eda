import matplotlib.pyplot as plt

plt.rcParams["backend"] = "TkAgg"
plt.ion()

fig, ax = plt.subplots(num="My chart window", clear=True)

ax.plot([1, 2, 3, 2, 3])
