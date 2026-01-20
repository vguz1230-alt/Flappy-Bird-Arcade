import arcade
import arcade.gui

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Главное меню"

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

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout(
            orientation="vertical",
            spacing=40,
            align="center"
        )

        play_button = arcade.gui.UIFlatButton(
            text="ИГРАТЬ",
            width=360,
            height=80,
            style=BUTTON_STYLE
        )
        play_button.on_click = self.on_click_play
        self.v_box.add(play_button)

        settings_button = arcade.gui.UIFlatButton(
            text="НАСТРОЙКИ",
            width=360,
            height=80,
            style=BUTTON_STYLE
        )
        settings_button.on_click = self.on_click_settings
        self.v_box.add(settings_button)

        exit_button = arcade.gui.UIFlatButton(
            text="ВЫХОД",
            width=360,
            height=80,
            style=BUTTON_STYLE
        )
        exit_button.on_click = self.on_click_exit
        self.v_box.add(exit_button)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(
            child=self.v_box,
            anchor_x="center_x",
            anchor_y="center_y"
        )
        self.manager.add(anchor)

        self.exit_dialog = None

    def on_click_play(self, event):
        print("Нажата кнопка ИГРАТЬ")

    def on_click_settings(self, event):
        print("Нажата кнопка НАСТРОЙКИ")

    def on_click_exit(self, event):
        if self.exit_dialog is not None:
            return

        self.exit_dialog = arcade.gui.UIMessageBox(
            width=420,
            height=220,
            message_text="Вы действительно хотите выйти?",
            buttons=[
                {
                    "text": "Да, выйти",
                    "style": {
                        "normal": arcade.gui.UIFlatButton.UIStyle(
                            font_size=20,
                            font_color=arcade.color.WHITE,
                            bg=arcade.color.DARK_RED,
                        ),
                        "hover": arcade.gui.UIFlatButton.UIStyle(
                            font_size=20,
                            font_color=arcade.color.WHITE,
                            bg=arcade.color.RED,
                        ),
                        "press": arcade.gui.UIFlatButton.UIStyle(
                            font_size=20,
                            font_color=arcade.color.WHITE,
                            bg=arcade.color.MAROON,
                        )
                    },
                    "callback": self.confirm_exit
                },
                {
                    "text": "Отмена",
                    "style": BUTTON_STYLE,
                    "callback": self.cancel_exit
                }
            ]
        )
        self.manager.add(self.exit_dialog)

    def confirm_exit(self, button):
        arcade.exit()

    def cancel_exit(self, button):
        self.manager.remove(self.exit_dialog)
        self.exit_dialog = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            SCREEN_TITLE,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 120,
            arcade.color.WHITE,
            font_size=52,
            anchor_x="center",
            font_name="Kenney Future"
        )
        self.manager.draw()

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
