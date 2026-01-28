import arcade
import arcade.gui
from gamescreen import GameView
from settings import SettingsView
from styles import BUTTON_STYLE, DIALOG_YES_STYLE, DIALOG_NO_STYLE

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Главное меню"

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
        anchor.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor)

        self.exit_dialog = None
        self.overlay = None

    def on_click_play(self, event):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

    def on_click_settings(self, event):
        settings_view = SettingsView()
        self.window.show_view(settings_view)

    def on_click_exit(self, event):
        if self.exit_dialog is not None:
            return

        self.v_box.visible = False

        overlay = arcade.gui.UIWidget(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        def render_overlay(surface):
            arcade.draw_lbwh_rectangle_filled(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0, 0, 180))
        overlay.do_render = render_overlay

        dialog_content = arcade.gui.UIBoxLayout(
            orientation="vertical",
            spacing=30,
            align="center"
        )

        dialog_content.add(arcade.gui.UISpace(height=30))

        message = arcade.gui.UILabel(
            text="Вы действительно хотите выйти?",
            text_color=arcade.color.WHITE,
            font_size=24,
            font_name="Arial",
            width=380,
            height=60,
            align="center"
        )
        dialog_content.add(message)

        dialog_content.add(arcade.gui.UISpace(height=20))

        buttons_hbox = arcade.gui.UIBoxLayout(
            orientation="horizontal",
            spacing=80,
            align="center"
        )

        yes_button = arcade.gui.UIFlatButton(
            text="Да, выйти",
            width=200,
            height=70,
            style=DIALOG_YES_STYLE
        )
        yes_button.on_click = self.confirm_exit
        buttons_hbox.add(yes_button)

        no_button = arcade.gui.UIFlatButton(
            text="Отмена",
            width=200,
            height=70,
            style=DIALOG_NO_STYLE
        )
        no_button.on_click = self.cancel_exit
        buttons_hbox.add(no_button)

        dialog_content.add(buttons_hbox)
        dialog_content.add(arcade.gui.UISpace(height=30))

        dialog_anchor = arcade.gui.UIAnchorLayout()
        dialog_anchor.add(child=dialog_content, anchor_x="center_x", anchor_y="center_y")

        self.overlay = overlay
        self.manager.add(self.overlay)

        self.exit_dialog = dialog_anchor
        self.manager.add(self.exit_dialog)

    def confirm_exit(self, event):
        arcade.exit()

    def cancel_exit(self, event):
        if self.exit_dialog:
            self.manager.remove(self.exit_dialog)
            self.exit_dialog = None
        if self.overlay:
            self.manager.remove(self.overlay)
            self.overlay = None

        self.v_box.visible = True

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
