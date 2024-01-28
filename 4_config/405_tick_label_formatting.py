import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import (
    MaxNLocator,
    EngFormatter,
    AutoLocator,
    LogitFormatter,
    PercentFormatter,
    ScalarFormatter,
    NullLocator,
)

import mpl_utils

mpl_utils.setup()

fig, ax = plt.subplots(num="Tick label formatting", clear=True)

x = np.linspace(start=0, stop=10, num=1000)
y = np.sin(x)

# Numerical x axis
# ax.plot(x, y)

# Date x axis
x_dates = pd.date_range(start="2000-01-01", periods=1000)
# ax.plot(x_dates, y)
series = pd.Series(data=y, index=x_dates)
series.plot(ax=ax)


ax.yaxis.set_major_locator(
    MaxNLocator(
        nbins=ax.yaxis.get_tick_space(),
        steps=[1, 2, 5],
    )
)


class MyEngFormatter(EngFormatter):
    ENG_PREFIXES = {
        0: "",
        3: "K",
        6: "M",
        9: "B",
        12: "T",
    }


# ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
# ax.yaxis.set_major_formatter(EngFormatter(sep=""))
# ax.yaxis.set_major_formatter(EngFormatter(sep="\N{HAIR SPACE}"))
# ax.yaxis.set_major_formatter(MyEngFormatter(sep="\N{HAIR SPACE}"))

# ax.yaxis.set_major_formatter("${x:,.0f}")


# def custom_formatter(x, pos):
#     text = f"${abs(x):,.2f}"
#     if x < 0:
#         return f"({text})"
#     return text
#
#
# ax.yaxis.set_major_formatter(custom_formatter)
