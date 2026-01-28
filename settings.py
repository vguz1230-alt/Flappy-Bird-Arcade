import arcade
import arcade.gui
import json
from styles import BUTTON_STYLE

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

SETTINGS_FILE = "settings.txt"

DEFAULT_SETTINGS = {
    "difficulty": "medium",
    "volume": 80,
    "skin": "robot"
}

class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.settings = self.load_settings()

        self.v_box = arcade.gui.UIBoxLayout(
            orientation="vertical",
            spacing=30,
            align="center"
        )

        title = arcade.gui.UILabel(
            text="НАСТРОЙКИ",
            text_color=arcade.color.WHITE,
            font_size=48,
            font_name="Kenney Future",
            width=400,
            height=80,
            align="center"
        )
        self.v_box.add(title)
        self.v_box.add(arcade.gui.UISpace(height=40))

        difficulty_label = arcade.gui.UILabel(
            text="Сложность игры:",
            text_color=arcade.color.WHITE,
            font_size=28,
            width=400
        )
        self.v_box.add(difficulty_label)

        difficulty_box = arcade.gui.UIBoxLayout(orientation="horizontal", spacing=20)
        for diff in ["Легко", "Средне", "Сложно"]:
            btn = arcade.gui.UIFlatButton(
                text=diff,
                width=180,
                height=60,
                style={
                    "normal": arcade.gui.UIFlatButton.UIStyle(bg=arcade.color.DARK_GRAY if diff.lower() != self.settings["difficulty"] else arcade.color.DARK_GREEN),
                    "hover": arcade.gui.UIFlatButton.UIStyle(bg=arcade.color.GRAY),
                    "press": arcade.gui.UIFlatButton.UIStyle(bg=arcade.color.DIM_GRAY)
                }
            )
            btn.difficulty = diff.lower().replace("легко", "easy").replace("средне", "medium").replace("сложно", "hard")
            btn.on_click = self.on_difficulty_click
            difficulty_box.add(btn)
        self.v_box.add(difficulty_box)
        self.v_box.add(arcade.gui.UISpace(height=30))

        volume_label = arcade.gui.UILabel(
            text=f"Громкость: {self.settings['volume']}%",
            text_color=arcade.color.WHITE,
            font_size=28,
            width=400
        )
        self.v_box.add(volume_label)

        volume_slider = arcade.gui.UISlider(
            min_value=0,
            max_value=100,
            value=self.settings["volume"],
            width=400,
            height=30
        )
        volume_slider.on_change = lambda e: self.on_volume_change(e, volume_label)
        self.v_box.add(volume_slider)
        self.v_box.add(arcade.gui.UISpace(height=40))

        skin_label = arcade.gui.UILabel(
            text="Скин персонажа:",
            text_color=arcade.color.WHITE,
            font_size=28,
            width=400
        )
        self.v_box.add(skin_label)

        skin_box = arcade.gui.UIBoxLayout(orientation="horizontal", spacing=20)
        skins = ["robot", "bird", "plane"]
        for skin in skins:
            btn = arcade.gui.UIFlatButton(
                text=skin.capitalize(),
                width=180,
                height=60,
                style={
                    "normal": arcade.gui.UIFlatButton.UIStyle(bg=arcade.color.DARK_GRAY if skin != self.settings["skin"] else arcade.color.DARK_BLUE),
                    "hover": arcade.gui.UIFlatButton.UIStyle(bg=arcade.color.GRAY),
                    "press": arcade.gui.UIFlatButton.UIStyle(bg=arcade.color.DIM_GRAY)
                }
            )
            btn.skin = skin
            btn.on_click = self.on_skin_click
            skin_box.add(btn)
        self.v_box.add(skin_box)
        self.v_box.add(arcade.gui.UISpace(height=50))

        back_button = arcade.gui.UIFlatButton(
            text="НАЗАД",
            width=300,
            height=80,
            style=BUTTON_STYLE
        )
        back_button.on_click = self.on_back_click
        self.v_box.add(back_button)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor)

    def load_settings(self):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return DEFAULT_SETTINGS.copy()

    def save_settings(self):
        print(f"Сохраняем настройки в {SETTINGS_FILE}")
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4, ensure_ascii=False)
        print("Настройки сохранены")

    def on_difficulty_click(self, event):
        btn = event.source
        self.settings["difficulty"] = btn.difficulty
        self.save_settings()
        for child in btn.parent.children:
            if hasattr(child, "difficulty"):
                child.style["normal"]["bg"] = arcade.color.DARK_GREEN if child.difficulty == self.settings["difficulty"] else arcade.color.DARK_GRAY

    def on_volume_change(self, event, label):
        value = int(event.new_value)
        self.settings["volume"] = value
        label.text = f"Громкость: {value}%"
        self.save_settings()

    def on_skin_click(self, event):
        btn = event.source
        self.settings["skin"] = btn.skin
        self.save_settings()
        for child in btn.parent.children:
            if hasattr(child, "skin"):
                child.style["normal"]["bg"] = arcade.color.DARK_BLUE if child.skin == self.settings["skin"] else arcade.color.DARK_GRAY

    def on_back_click(self, event):
        self.window.show_view(self.window.menu_view)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "НАСТРОЙКИ",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 120,
            arcade.color.WHITE,
            font_size=52,
            anchor_x="center",
            font_name="Kenney Future"
        )
        self.manager.draw()