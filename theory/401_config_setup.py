from matplotlib import pyplot as plt


def setup():
    plt.rcParams.update(
        {
            "backend": "TkAgg",
            "interactive": True,
            "figure.constrained_layout.use": True,
        }
    )


if __name__ == "__main__":
    setup()

    fig, ax = plt.subplots(num="Chart", clear=True)
    # ax.plot([1, 2, 3, 2])
    ax.plot([1, 2, 3, 2, 3], label="A line")
    ax.legend()
    ax.set(
        title="My axes",
        xlabel="X label",
        ylabel="Y label",
    )
