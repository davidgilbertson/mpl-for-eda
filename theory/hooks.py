def configure_figure(fig):
    try:
        fig.canvas.manager.window.geometry("640x522+2976+402")
    except AttributeError:
        pass
