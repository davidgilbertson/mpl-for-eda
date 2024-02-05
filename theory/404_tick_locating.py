import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd

import mpl_utils

df = pd.read_csv("../data/crop-data.csv")
chart_df = df[df.Country.eq("Niue") & df.Crop.eq("Cassava")]

mpl_utils.setup()
# plt.rcParams["axes.autolimit_mode"] = "round_numbers"
fig, ax = plt.subplots(num="Tick locators", clear=True)

ax.plot(chart_df.Year, chart_df.Yield)
ax.set_ylim(0)

ax.yaxis.set_major_locator(
    MaxNLocator(
        nbins=ax.yaxis.get_tick_space(),
        steps=[1, 2, 5],
    )
)
