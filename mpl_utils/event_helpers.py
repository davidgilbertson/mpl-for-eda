import math

from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseButton, MouseEvent


# Added in #509
class AxesEventHandlers:
    def __init__(self, ax: Axes):
        self.ax = ax
        ax.figure.canvas.mpl_connect("button_press_event", self._on_button_press)
        ax.figure.canvas.mpl_connect("button_release_event", self._on_button_release)
        ax.figure.canvas.mpl_connect("axes_leave_event", self._on_ax_leave)
        ax.figure.canvas.mpl_connect("figure_leave_event", self.on_leave)

        ax._axes_event_handlers_ref = self

    def _on_button_press(self, event: MouseEvent):
        self._button_press_xy = (event.x, event.y)

    def _on_button_release(self, event: MouseEvent):
        if event.inaxes != self.ax:
            return

        if math.dist(self._button_press_xy, (event.x, event.y)) > 5:
            return  # A drag

        if event.button == MouseButton.LEFT:
            self.on_left_click(event)

        if event.button == MouseButton.RIGHT:
            self.on_right_click(event)

    def _on_ax_leave(self, event):
        if event.inaxes == self.ax:
            self.on_leave(event)

    def on_left_click(self, event):
        pass

    def on_right_click(self, event):
        pass

    def on_leave(self, event):
        pass
