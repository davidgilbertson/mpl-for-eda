from matplotlib import pyplot as plt


# This is called as a hook when a figure is created
def configure_figure(fig):
    try:
        fig.canvas.manager.window.geometry("840x1054+2874+297")
    except AttributeError:
        pass


def setup(font_bump=1):
    plt.rcdefaults()

    # This cycler will cycle through the default colors with a plain line,
    # then again for a dashed line, and again for a dotted line
    prop_cycle = (
        plt.cycler("linestyle", ["-", "--", ":", "-."])
        * plt.rcParams["axes.prop_cycle"]
    )

    blue_gray_100 = "#cfd8dc"
    blue_gray_300 = "#90a4ae"
    blue_gray_700 = "#455a64"
    blue_gray_900 = "#263238"
    blue_gray_950 = "#1d272b"

    plt.rcParams.update(
        {
            # Window config
            "backend": "TkAgg",
            "interactive": True,
            # Layout
            "figure.figsize": (10, 10),  # Avoid constrained layout collapsing to zero
            "figure.constrained_layout.use": True,
            "figure.constrained_layout.h_pad": 0.1,
            "figure.constrained_layout.w_pad": 0.1,
            "figure.constrained_layout.hspace": 0.1,
            "figure.constrained_layout.wspace": 0.05,
            # Styles
            "font.size": 10 + font_bump,
            "figure.facecolor": blue_gray_950,
            "axes.facecolor": blue_gray_950,
            "text.color": blue_gray_100,
            "axes.labelcolor": blue_gray_300,
            "axes.grid": True,
            "grid.color": blue_gray_900,
            "axes.edgecolor": blue_gray_700,  # used by spines
            "axes.linewidth": 1,  # used by spines
            "axes.spines.top": False,
            "axes.spines.left": False,
            "axes.spines.right": False,
            "axes.spines.bottom": False,
            "figure.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.titlepad": 12,
            "axes.titleweight": "bold",
            "axes.labelpad": 12 + font_bump,
            "xtick.bottom": False,
            "ytick.left": False,
            "ytick.right": False,
            "xtick.major.size": 0,
            "ytick.major.size": 0,
            "xtick.minor.size": 0,
            "ytick.minor.size": 0,
            "xtick.color": blue_gray_300,
            "ytick.color": blue_gray_300,
            # Other
            "axes.prop_cycle": prop_cycle,
            "axes.xmargin": 0.01,
            "axes.ymargin": 0.02,
            "date.converter": "concise",
            "axes.axisbelow": True,  # grid lines behind chart elements
            "legend.columnspacing": 1,
            "hist.bins": "auto",
            "scatter.edgecolors": "none",
            "patch.facecolor": blue_gray_900,  # used by tooltip
            "patch.edgecolor": blue_gray_700,
            "patch.linewidth": 0.5,
            "figure.hooks": "403_hooks:configure_figure",
        }
    )


if __name__ == "__main__":
    setup()

    fig, ax = plt.subplots(num="My chart", clear=True)

    for i in range(15):
        ax.plot([0, i], label=f"Line {i}")

    ax.legend()
