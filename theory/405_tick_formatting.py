import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import EngFormatter, PercentFormatter

import mpl_utils


df = pd.read_csv("../data/crop-data.csv", parse_dates=["Year"])
chart_df = df[df.Country.eq("Cuba") & df.Crop.eq("Cocoa")]

mpl_utils.setup()
fig, ax = plt.subplots(num="Tick formatters", clear=True)

# ScalarFormatter
ax.plot(chart_df.Year, chart_df.Yield)

# PercentFormatter
# ax.plot(chart_df.Year, chart_df.Yield / chart_df.Yield.max())
# ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))

# EngFormatter
# ax.plot(chart_df.Year, chart_df.Population)
# ax.yaxis.set_major_formatter(EngFormatter())

# String formatter
# ax.plot(chart_df.Year, chart_df.GDPPC)
# ax.yaxis.set_major_formatter("${x:,.0f}")

# Pandas formatter
# chart_df.plot(ax=ax, x="Year", y="Yield")
