import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import EngFormatter, PercentFormatter

import mpl_utils


class MyEngFormatter(EngFormatter):
    ENG_PREFIXES = {
        0: "",
        3: "K",
        6: "M",
        9: "B",
        12: "T",
    }


df = pd.read_csv("../data/crop-data.csv", parse_dates=["Year"])
chart_df = df[df.Country.eq("China") & df.Crop.eq("Rice")]

mpl_utils.setup()
fig, ax = plt.subplots(num="Tick label formatting", clear=True)

ax.plot(chart_df.Year, chart_df.Yield)

# ax.plot(chart_df.Year, chart_df.Yield / chart_df.Yield.max())
# ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))

# ax.plot(chart_df.Year, chart_df.Population)
# ax.yaxis.set_major_formatter(EngFormatter())
# ax.yaxis.set_major_formatter(EngFormatter(sep=""))
# ax.yaxis.set_major_formatter(EngFormatter(sep="\N{HAIR SPACE}"))
# ax.yaxis.set_major_formatter(MyEngFormatter(sep="\N{HAIR SPACE}"))

# ax.plot(chart_df.Year, chart_df.GDPPC)
# ax.yaxis.set_major_formatter("${x:,.0f}")

# chart_df.plot(x="Year", y="Yield", ax=ax)
