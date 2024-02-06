from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.offsetbox import AnchoredText, AnchoredOffsetbox, VPacker, TextArea
from matplotlib.transforms import IdentityTransform

import mpl_utils

mpl_utils.setup()
fig, ax = plt.subplots(num="Text options", clear=True)
mpl_utils.add_text_zoom()
ax: Axes

ax.scatter(
    [400, 400, 400, 400],
    [200, 400, 600, 800],
    transform=IdentityTransform(),
)
ax.set_axis_off()

text = ax.text(
    x=400 + 15,
    y=800 + 15,
    s="My Text",
    bbox={},
    transform=IdentityTransform(),
)

ann = ax.annotate(
    xy=(400, 600),
    text="My Annotation",
    xycoords="figure pixels",
    xytext=(15, 15),
    textcoords="offset pixels",
    bbox={},
)

anchored_text = AnchoredText(
    s="My AnchoredText",
    bbox_to_anchor=(400, 400),
    loc="lower left",
    prop=dict(bbox={}),
    frameon=False,
)

ax.add_artist(anchored_text)

offset_box = AnchoredOffsetbox(
    bbox_to_anchor=(400, 200),
    loc="lower left",
    child=VPacker(
        children=[
            TextArea("I'm bold", textprops=dict(weight="bold")),
            TextArea("I'm italic", textprops=dict(style="italic")),
            TextArea("I'm salmon", textprops=dict(color="xkcd:salmon")),
        ],
    ),
)
offset_box.patch.set(
    facecolor=plt.rcParams["patch.facecolor"],
    edgecolor=plt.rcParams["patch.edgecolor"],
)
ax.add_artist(offset_box)
