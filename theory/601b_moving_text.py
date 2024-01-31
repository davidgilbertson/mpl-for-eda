from matplotlib import pyplot as plt
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.figure import Figure
from matplotlib.offsetbox import AnchoredText, AnchoredOffsetbox, VPacker, TextArea
from matplotlib.patheffects import withSimplePatchShadow
from matplotlib.text import Annotation, Text

import mpl_utils


class Blitter:
    def __init__(self, fig: Figure):
        self.fig = fig
        self.canvas = fig.canvas
        self.background = None
        self.capture_background()

        fig.canvas.mpl_connect("figure_leave_event", self.restore_background)
        fig.canvas.mpl_connect("draw_event", self.capture_background)

    def capture_background(self, _=None):
        self.background = self.canvas.copy_from_bbox(self.fig.bbox)

    def blit(self, artist: Artist):
        self.canvas.restore_region(self.background)
        self.fig.draw_artist(artist)
        self.canvas.blit()

    def restore_background(self, _=None):
        self.canvas.restore_region(self.background)
        self.canvas.blit()
        self.canvas.flush_events()


class TextOptionsDemo:
    fig: Figure
    tl_ax: Axes
    tr_ax: Axes
    bl_ax: Axes
    br_ax: Axes
    text: Text
    ann: Annotation
    anchored_text: AnchoredText
    offset_box: AnchoredOffsetbox

    def __init__(self):
        mpl_utils.setup()
        self.fig, ((self.tl_ax, self.tr_ax), (self.bl_ax, self.br_ax)) = plt.subplots(
            num="Text options - moving",
            clear=True,
            nrows=2,
            ncols=2,
        )
        mpl_utils.clear_events()

        self.offset = 15

        self.tl_ax.set_title("Text")
        self.tr_ax.set_title("Annotation")
        self.bl_ax.set_title("AnchoredText")
        self.br_ax.set_title("AnchoredOffsetbox")

        self.add_text()
        self.add_annotation()
        self.add_anchored_text()
        self.offset_box = None

        self.fig.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)
        self.blitter = Blitter(self.fig)
        self.fig._TextOptionsDemo_ref = self

    def add_text(self):
        self.text = self.tl_ax.text(
            x=0,
            y=0,
            transform=None,
            s="Text",
            in_layout=False,
            bbox=dict(
                alpha=0.8,
                path_effects=[withSimplePatchShadow(offset=(2, -2))],
            ),
            linespacing=1.5,
            animated=True,
        )

    def offsets_from_event(self, event):
        ax_x, ax_y = event.inaxes.transAxes.inverted().transform((event.x, event.y))
        x_offset = self.offset if ax_x < 0.5 else -self.offset
        y_offset = self.offset if ax_y < 0.5 else -self.offset
        ha = "left" if ax_x < 0.5 else "right"
        va = "bottom" if ax_y < 0.5 else "top"
        return x_offset, y_offset, ha, va

    def set_text_position(self, event):
        x, y = event.x, event.y
        x_offset, y_offset, ha, va = self.offsets_from_event(event)
        self.text.set(
            text=f"Text\n{x, y}",
            x=x + x_offset,
            y=y + y_offset,
            ha=ha,
            va=va,
        )
        return self.text

    def add_annotation(self):
        self.ann = self.tr_ax.annotate(
            text="Annotation",
            xy=(0, 0),
            xycoords="figure pixels",
            xytext=(self.offset, self.offset),
            textcoords="offset pixels",
            in_layout=False,
            bbox=dict(
                alpha=0.8,
                path_effects=[withSimplePatchShadow(offset=(2, -2))],
            ),
            linespacing=1.5,
            animated=True,
        )

    def set_annotation_position(self, event):
        x, y = event.x, event.y
        ax_x, ax_y = event.inaxes.transAxes.inverted().transform((x, y))

        self.ann.xy = (x, y)
        self.ann.set(
            text=f"Annotation\n{x, y}",
            x=self.offset if ax_x < 0.5 else -self.offset,
            y=self.offset if ax_y < 0.5 else -self.offset,
            ha="left" if ax_x < 0.5 else "right",
            va="bottom" if ax_y < 0.5 else "top",
        )
        return self.ann

    def add_anchored_text(self):
        self.anchored_text = AnchoredText(
            s="",
            bbox_to_anchor=(200, 100),
            loc="lower left",
            frameon=False,  # hide the default patch (wrong colors)
            prop=dict(
                bbox=dict(  # use the Text patch instead
                    alpha=0.8,
                    path_effects=[withSimplePatchShadow(offset=(2, -2))],
                ),
                linespacing=1.5,
            ),
            animated=True,
        )
        self.fig.add_artist(self.anchored_text)

    def set_anchored_text_position(self, event):
        x, y = event.x, event.y
        self.anchored_text.set_bbox_to_anchor((x, y))
        self.anchored_text.txt.set_text(f"AnchoredText\n{x, y}")
        self.anchored_text.loc = self.anchored_text.codes[self.loc_from_event(event)]

        return self.anchored_text

    def set_offset_box_position(self, event):
        # We don't 'move' an offset box, we delete it and create a new one
        if self.offset_box:
            self.offset_box.remove()

        x, y = event.x, event.y

        self.offset_box = AnchoredOffsetbox(
            bbox_to_anchor=(x, y),
            loc=self.loc_from_event(event),
            child=VPacker(
                children=[
                    TextArea("AnchoredOffsetbox", textprops=dict(weight="bold")),
                    TextArea(f"{x = }", textprops=dict(color="tab:blue")),
                    TextArea(f"{y = }", textprops=dict(color="tab:orange")),
                ],
                sep=3,
            ),
            animated=True,
        )
        self.offset_box.patch.set(
            facecolor=plt.rcParams["patch.facecolor"],
            edgecolor=plt.rcParams["patch.edgecolor"],
            alpha=0.8,
            path_effects=[withSimplePatchShadow(offset=(2, -2))],
        )
        self.fig.add_artist(self.offset_box)

        return self.offset_box

    @staticmethod
    def loc_from_event(event: MouseEvent):
        if not event.inaxes:
            return

        ax_x, ax_y = event.inaxes.transAxes.inverted().transform((event.x, event.y))
        anchor_corner = "lower" if ax_y < 0.5 else "upper"
        anchor_corner += " left" if ax_x < 0.5 else " right"
        return anchor_corner

    def on_mouse_move(self, event: MouseEvent):
        method = None
        if event.inaxes == self.tl_ax:
            method = self.set_text_position
        elif event.inaxes == self.tr_ax:
            method = self.set_annotation_position
        elif event.inaxes == self.bl_ax:
            method = self.set_anchored_text_position
        elif event.inaxes == self.br_ax:
            method = self.set_offset_box_position

        if method:
            updated_artist = method(event)

            self.blitter.blit(updated_artist)
        else:
            self.blitter.restore_background()


TextOptionsDemo()
