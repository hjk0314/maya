import pymel.core as pm


class ShapeColorPaletteUI:
    """ A UI tool for setting the overrideColor index of selected shapes 
    in Maya using a compact and neatly padded RGB palette grid.

    Examples
    --------
    >>> palette_ui = ShapeColorPaletteUI()
    >>> palette_ui.show()
     """
    COLOR_PALETTE = {
        "gray": (0.534, 0.534, 0.534), 
        "black": (0.0, 0.0, 0.0), 
        "dark_gray": (0.332, 0.332, 0.332), 
        "medium_gray": (0.662, 0.662, 0.662), 
        "brick_red": (0.607, 0.258, 0.234), 
        "indigo": (0.17, 0.095, 0.44), 
        "blue": (0.0, 0.0, 1.0), 
        "olive_green": (0.242, 0.345, 0.184), 
        "dark_violet": (0.209, 0.096, 0.334), 
        "light_purple": (0.744, 0.33, 0.871), 
        "brown": (0.55, 0.384, 0.287), 
        "dark_brown": (0.299, 0.217, 0.189), 
        "rust": (0.595, 0.297, 0.118), 
        "red": (1.0, 0.0, 0.0), 
        "lime_green": (0.0, 1.0, 0.0), 
        "periwinkle": (0.295, 0.336, 0.645), 
        "white": (1.0, 1.0, 1.0), 
        "yellow": (1.0, 1.0, 0.0), 
        "light_cyan": (0.673, 1.0, 1.0), 
        "pale_green": (0.616, 1.0, 0.648), 
        "light_pink": (1.0, 0.78, 0.761), 
        "peach": (1.0, 0.76, 0.545), 
        "chartreuse": (0.840, 1.0, 0.0), 
        "forest_green": (0.443, 0.645, 0.426), 
        "tan": (0.631, 0.497, 0.291), 
        "khaki": (0.675, 0.693, 0.324), 
        "sage_green": (0.548, 0.683, 0.324), 
        "moss_green": (0.476, 0.679, 0.455), 
        "teal_blue": (0.49, 0.68, 0.695), 
        "slate_blue": (0.392, 0.469, 0.683), 
        "lavender_gray": (0.468, 0.304, 0.678), 
        "rose": (0.608, 0.333, 0.478), 
        }
    WINDOW_NAME = "shapeColorPaletteWin"


    def __init__(self):
        """ Initialize the palette UI and selection state. """
        self.palette_items = list(self.COLOR_PALETTE.items())
        self.selected_idx = 0


    def select_color(self, idx, *args):
        """ Set the currently selected palette color index.

        Args:
            idx (int): The palette color index.
         """
        self.selected_idx = idx


    def apply_palette_color(self, *args):
        """ Apply the selected color index to the overrideColor 
        of all selected shapes in Maya.
         """
        idx = self.selected_idx
        sel = pm.selected()
        if not sel:
            pm.warning("Please select a controller.")
            return
        for obj in sel:
            shapes = obj.getShapes(noIntermediate=True)
            for shape in shapes:
                if shape.hasAttr('overrideEnabled'):
                    shape.overrideEnabled.set(1)
                    shape.overrideRGBColors.set(0)
                    shape.overrideColor.set(idx)
        pm.inViewMessage(amg="Color index applied.", pos="topCenter", f=True)


    def close(self, *args):
        """ Close the palette UI window. """
        if pm.window(self.WINDOW_NAME, exists=True):
            pm.deleteUI(self.WINDOW_NAME)


    def show(self):
        """ Display the color palette UI with balanced padding. """
        if pm.window(self.WINDOW_NAME, exists=True):
            pm.deleteUI(self.WINDOW_NAME)
        grid_rows = 4
        grid_cols = 8
        grid_btn_h = 20
        grid_btn_w = 26
        btn_h = 22
        side_padding = 4
        top_padding = 2
        bottom_padding = 10

        window_w = (grid_cols * grid_btn_w) + (side_padding * 2)
        window_h = (grid_rows * grid_btn_h) + (2 * btn_h) 
        window_h += top_padding + bottom_padding + 18

        win = pm.window(
            self.WINDOW_NAME,
            title="Shape Color Palette",
            width=window_w,
            height=window_h,
            sizeable=False
        )
        pm.showWindow(win)
        pm.setParent(win)
        pm.columnLayout(adj=True, rs=3, cat=("both", side_padding))
        pm.separator(h=top_padding, style='none')

        pm.frameLayout(lv=False, mw=0, mh=0, bv=False)
        pm.gridLayout(nc=grid_cols, cw=grid_btn_w, ch=grid_btn_h)
        for idx, (name, rgb) in enumerate(self.palette_items):
            pm.button(
                label="",
                bgc=rgb,
                c=pm.Callback(self.select_color, idx),
                ann=f"{name}: index={idx}, rgb={rgb}"
            )
        pm.setParent('..')
        pm.setParent('..')

        pm.separator(h=8, style='none')
        pm.button(label="Apply", height=btn_h, c=self.apply_palette_color)
        pm.button(label="Close", height=btn_h, c=self.close)
        pm.separator(h=10, style='none')
        pm.setParent('..')
        pm.setParent('..')


ShapeColorPaletteUI().show()

