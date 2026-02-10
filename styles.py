import arcade.gui

BUTTON_STYLE = {
    "normal": arcade.gui.UIFlatButton.UIStyle(
        font_size=24,
        font_name="Arial",
        font_color=arcade.color.WHITE,
        bg=arcade.color.DARK_BLUE_GRAY,
        border_width=2
    ),
    "hover": arcade.gui.UIFlatButton.UIStyle(
        font_size=24,
        font_name="Arial",
        font_color=arcade.color.WHITE,
        bg=arcade.color.DARK_SLATE_BLUE,
        border_width=2
    ),
    "press": arcade.gui.UIFlatButton.UIStyle(
        font_size=24,
        font_name="Arial",
        font_color=arcade.color.WHITE,
        bg=arcade.color.DARK_GRAY,
        border_width=2
    ),
}

DIALOG_YES_STYLE = {
    "normal": arcade.gui.UIFlatButton.UIStyle(
        font_size=20,
        font_name="Arial",
        font_color=arcade.color.WHITE,
        bg=arcade.color.DARK_RED,
        border_width=2
    ),
    "hover": arcade.gui.UIFlatButton.UIStyle(
        font_size=20,
        font_name="Arial",
        font_color=arcade.color.WHITE,
        bg=arcade.color.RED,
        border_width=2
    ),
    "press": arcade.gui.UIFlatButton.UIStyle(
        font_size=20,
        font_name="Arial",
        font_color=arcade.color.WHITE,
        bg=arcade.color.MAROON,
        border_width=2
    ),
}

DIALOG_NO_STYLE = {
    "normal": arcade.gui.UIFlatButton.UIStyle(
        font_size=20,
        font_name="Arial",
        font_color=arcade.color.WHITE,
        bg=arcade.color.DARK_GRAY,
        border_width=2
    ),
    "hover": arcade.gui.UIFlatButton.UIStyle(
        font_size=20,
        font_name="Arial",
        font_color=arcade.color.WHITE,
        bg=arcade.color.GRAY,
        border_width=2
    ),
    "press": arcade.gui.UIFlatButton.UIStyle(
        font_size=20,
        font_name="Arial",
        font_color=arcade.color.WHITE,
        bg=arcade.color.DIM_GRAY,
        border_width=2
    ),
}