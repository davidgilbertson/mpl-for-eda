from collections.abc import Iterable, Callable
from itertools import zip_longest
from typing import Any

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.transforms import IdentityTransform
from matplotlib.widgets import Button
import pandas as pd

import mpl_utils


def batched(items: Iterable, n) -> list[list]:
    if not isinstance(items, list):
        items = list(items)

    batch_starts = range(0, len(items), n)
    return [items[i : i + n] for i in batch_starts]


# Added in #804
class plot_paginated:
    def __init__(
        self,
        items: Iterable[Any],
        render: Callable[[Axes, Any], None],
        filter_predicate: Callable[[Any, str], bool] = None,
        items_per_page=5,
        title="Paginator",
    ):
        self.items = items
        self.render = render
        self.filter_predicate = filter_predicate
        self.items_per_page = items_per_page

        self.fig, axs = mpl_utils.flex_subplots(
            title,
            row_heights=[1] * items_per_page + ["40px"],
        )

        axs[-1].set_axis_off()
        self.axs = axs[:-1]

        self.paged_items = batched(items, items_per_page)
        self.curr_page_index = 0
        self.curr_page_items = self.paged_items[self.curr_page_index]

        self.prev_button = Button(
            ax=mpl_utils.add_axes_px((10, 10, 30, 30)),
            label="◀",
            color=plt.rcParams["grid.color"],
            hovercolor=plt.rcParams["axes.edgecolor"],
        )
        self.prev_button.on_clicked(lambda event: self.change_page(-1))

        self.page_text = self.fig.text(
            x=80,
            y=25,
            transform=IdentityTransform(),
            s="",
            ha="center",
            va="center_baseline",
        )

        self.next_button = Button(
            ax=mpl_utils.add_axes_px((120, 10, 30, 30)),
            label="▶",
            color=plt.rcParams["grid.color"],
            hovercolor=plt.rcParams["axes.edgecolor"],
        )
        self.next_button.on_clicked(lambda event: self.change_page(1))

        if filter_predicate:
            self.search_box = mpl_utils.add_text_box(
                origin="bottom right",
                bounds=(10, 10, 200, 30),
                label="Search: ",
                on_change=self.on_search_change,
            )

        self.render_page()

        self.fig._plot_paginated_ref = self

    def on_search_change(self, text):
        if text == "":
            filtered_items = self.items
        else:
            filtered_items = [
                item for item in self.items if self.filter_predicate(item, text)
            ]

        self.paged_items = batched(filtered_items, self.items_per_page)
        self.curr_page_index = 0
        if self.paged_items:
            self.curr_page_items = self.paged_items[self.curr_page_index]
        else:
            self.curr_page_items = []

        self.render_page()

    def change_page(self, shift: int):
        if not self.paged_items:
            return

        self.curr_page_index = (self.curr_page_index + shift) % len(self.paged_items)
        self.curr_page_items = self.paged_items[self.curr_page_index]

        self.render_page()

    def render_page(self):
        for item, ax in zip_longest(self.curr_page_items, self.axs):
            ax.clear()

            if item is None:
                ax.set_axis_off()
                continue

            self.render(ax, item)

        self.page_text.set_text(
            f"{self.curr_page_index + 1} of {len(self.paged_items)}"
        )
        self.fig.canvas.draw_idle()


if __name__ == "__main__":
    df = pd.read_csv("../../data/crop-data.csv")

    def render(ax: Axes, item: tuple[str, pd.DataFrame]):
        item_name, item_df = item
        chart_df = item_df.pivot_table(
            index="Year",
            columns="Crop",
            values="Yield",
        )
        ax.plot(chart_df, label=chart_df.columns)
        ax.legend(
            loc="lower right",
            bbox_to_anchor=(1, 1),
            ncols=5,
            frameon=False,
        )
        ax.set_title(item_name)

    self = plot_paginated(
        items=df.groupby("Country"),
        render=render,
        filter_predicate=lambda item, text: text.lower() in item[0].lower(),
    )
    self.fig.suptitle("Yield by country and crop")
