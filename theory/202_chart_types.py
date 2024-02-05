import matplotlib.pyplot as plt

fig, ax = plt.subplots()

# ax.plot(
#     [1, 2, 3, 2, 3],
#     color="red",
#     linestyle="dashed",
# )

# ax.scatter(
#     x=[1, 2, 3],
#     y=[2, 2, 1],
# )

# ax.bar(
#     x=[1, 2, 3],
#     height=[2, 2, 1],
# )

ax.bar(
    x=[1, 2, 3],
    height=[2, 2, 1],
    color="red",
    edgecolor="black",
)

plt.show()
