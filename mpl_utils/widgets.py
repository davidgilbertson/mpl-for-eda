from collections.abc import Callable
from typing import Literal

from matplotlib import pyplot as plt
from matplotlib.backend_bases import KeyEvent
from matplotlib.widgets import TextBox

import mpl_utils


def add_text_box(
    bounds: tuple[float, float, float, float],
    on_change: Callable[[str], None],
    origin: Literal[
        "top left",
        "top right",
        "bottom left",
        "bottom right",
    ] = "bottom left",
    label="",
    fig=None,
    **kwargs,
):
    fig = fig or plt.gcf()

    text_box = TextBox(
        ax=mpl_utils.add_axes_px(bounds=bounds, origin=origin, fig=fig),
        label=label,
        color=plt.rcParams["grid.color"],
        hovercolor=plt.rcParams["axes.edgecolor"],
        **kwargs,
    )
    text_box.cursor.set_color(plt.rcParams["text.color"])
    text_box.on_text_change(on_change)

    def on_key_press(event: KeyEvent):
        if event.key == "escape" and text_box.capturekeystrokes:
            text_box.set_val("")

    fig.canvas.mpl_connect("key_press_event", on_key_press)

    return text_box
