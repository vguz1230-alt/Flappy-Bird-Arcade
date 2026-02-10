import arcade
import random
import json

BASE_GRAVITY = 0.4
BASE_JUMP_POWER = 9
BASE_PIPE_SPEED = 3.8
BASE_PIPE_WIDTH = 90
BASE_PIPE_INTERVAL = 1.9

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.load_settings()

        arcade.set_background_color(arcade.color.SKY_BLUE)

        skin_paths = {
            "robot": ":resources:images/animated_characters/robot/robot_idle.png",
            "bird": ":resources:images/birds/bluebird-midflap.png",
            "plane": ":resources:images/space_shooter/playerShip1_blue.png"
        }
        skin_path = skin_paths.get(self.skin, skin_paths["robot"])

        self.player = arcade.Sprite(skin_path, scale=0.6)
        self.player.center_x = 250
        self.player.center_y = self.window.height // 2
        self.player.velocity_y = 0

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.pipe_list = arcade.SpriteList()

        self.last_pipe_time = 0.0
        self.last_update_time = 0.0

        self.score = 0
        self.score_text = arcade.Text(
            "0",
            self.window.width // 2,
            self.window.height - 80,
            arcade.color.WHITE,
            72,
            font_name="Kenney Future",
            anchor_x="center",
            anchor_y="center"
        )

        self.game_started = False
        self.game_over = False

        self.ready_text = arcade.Text(
            "Нажми ЛКМ или ПРОБЕЛ",
            self.window.width // 2,
            self.window.height // 2,
            arcade.color.WHITE,
            40,
            font_name="Arial",
            anchor_x="center",
            anchor_y="center"
        )

        self.game_over_text = arcade.Text(
            "ИГРА ОКОНЧЕНА",
            self.window.width // 2,
            self.window.height // 2 + 80,
            arcade.color.RED,
            60,
            font_name="Kenney Future",
            anchor_x="center",
            anchor_y="center"
        )

        self.final_score_text = arcade.Text(
            "",
            self.window.width // 2,
            self.window.height // 2,
            arcade.color.WHITE,
            48,
            font_name="Arial",
            anchor_x="center",
            anchor_y="center"
        )

    def load_settings(self):
        try:
            with open("settings.txt", "r", encoding="utf-8") as f:
                settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            settings = {
                "difficulty": "medium",
                "volume": 80,
                "skin": "robot"
            }

        self.gravity = BASE_GRAVITY

        diff = settings.get("difficulty", "medium")
        self.difficulty = diff  # ← добавь эту строку!

        if diff == "easy":
            self.pipe_interval = 2.5
            self.pipe_gap = 240
        elif diff == "medium":
            self.pipe_interval = BASE_PIPE_INTERVAL
            self.pipe_gap = 220
        else:  # hard
            self.pipe_interval = 1.5
            self.pipe_gap = 180

        self.volume = settings.get("volume", 80)
        self.skin = settings.get("skin", "robot")

    def setup(self):
        self.player.center_y = self.window.height // 2
        self.player.velocity_y = 0
        self.score = 0
        self.score_text.text = "0"
        self.pipe_list.clear()
        self.last_pipe_time = 0.0
        self.last_update_time = 0.0
        self.game_started = False
        self.game_over = False

    def on_show_view(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_update(self, delta_time: float):
        if not self.game_started or self.game_over:
            return

        self.player.velocity_y -= self.gravity
        self.player.center_y += self.player.velocity_y

        if self.player.top < 0 or self.player.bottom > self.window.height:
            self.game_over = True
            self.final_score_text.text = f"Счёт: {self.score}"
            return

        for pipe in self.pipe_list:
            pipe.center_x -= BASE_PIPE_SPEED

        while len(self.pipe_list) >= 2 and self.pipe_list[0].right < 0:
            self.pipe_list.pop(0)
            self.pipe_list.pop(0)
            self.score += 1
            self.score_text.text = str(self.score)

        self.last_update_time += delta_time
        if self.last_update_time - self.last_pipe_time > self.pipe_interval:
            self.spawn_pipe()
            self.last_pipe_time = self.last_update_time

        self.check_collisions()

    def spawn_pipe(self):
        min_y = 140
        max_y = self.window.height - 140 - self.pipe_gap

        # На hard — зазор не может сильно отличаться от предыдущего
        if self.difficulty == "hard" and hasattr(self, 'last_gap_y'):
            half = self.window.height // 2
            prev = self.last_gap_y

            if prev < half:
                min_y = 140
                max_y = half - self.pipe_gap // 2
            else:
                min_y = half + self.pipe_gap // 2
                max_y = self.window.height - 140 - self.pipe_gap

            if min_y >= max_y:
                min_y = 140
                max_y = self.window.height - 140 - self.pipe_gap

        gap_y = random.randint(min_y, max_y)

        top_pipe = arcade.SpriteSolidColor(BASE_PIPE_WIDTH, self.window.height, arcade.color.FOREST_GREEN)
        top_pipe.center_x = self.window.width + 200
        top_pipe.bottom = gap_y + self.pipe_gap

        bottom_pipe = arcade.SpriteSolidColor(BASE_PIPE_WIDTH, self.window.height, arcade.color.FOREST_GREEN)
        bottom_pipe.center_x = self.window.width + 200
        bottom_pipe.top = gap_y

        self.pipe_list.append(top_pipe)
        self.pipe_list.append(bottom_pipe)

        self.last_gap_y = gap_y  # запоминаем


    def check_collisions(self):
        for pipe in self.pipe_list:
            if arcade.check_for_collision(self.player, pipe):
                self.game_over = True
                self.final_score_text.text = f"Счёт: {self.score}"
                break

    def on_key_press(self, symbol: int, modifiers: int):
        if self.game_over:
            if symbol in (arcade.key.ESCAPE, arcade.key.ENTER, arcade.key.RETURN):
                self.window.show_view(self.window.menu_view)
            return

        if not self.game_started:
            self.game_started = True
            return

        if symbol in (arcade.key.SPACE, arcade.key.UP):
            self.player.velocity_y = BASE_JUMP_POWER

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.game_over:
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.setup()
            return

        if not self.game_started:
            self.game_started = True
            return

        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player.velocity_y = BASE_JUMP_POWER

    def on_draw(self):
        self.clear()

        # Сначала фон и трубы (нижний слой)
        if self.game_started and not self.game_over:
            self.pipe_list.draw()

        # Птичка поверх труб
        self.player_list.draw()

        # Счёт поверх всего
        self.score_text.draw()

        # Надпись "готов к старту" — тоже поверх
        if not self.game_started:
            self.ready_text.draw()

        # Экран game over — самый верхний слой
        if self.game_over:
            arcade.draw_lbwh_rectangle_filled(
                0, 0,
                self.window.width, self.window.height,
                (0, 0, 0, 140)
            )
            self.game_over_text.draw()
            self.final_score_text.draw()

            arcade.draw_text(
                "ЛКМ — Перезапустить",
                self.window.width // 2, self.window.height // 2 - 60,
                arcade.color.WHITE, 28, anchor_x="center"
            )
            arcade.draw_text(
                "ESC / ENTER — В меню",
                self.window.width // 2, self.window.height // 2 - 100,
                arcade.color.WHITE, 28, anchor_x="center"
            )