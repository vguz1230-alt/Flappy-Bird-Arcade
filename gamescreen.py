import arcade
import random
import json

BASE_GRAVITY = 0.4
BASE_JUMP_POWER = 9
BASE_PIPE_SPEED = 3.8
BASE_PIPE_WIDTH = 90
BASE_PIPE_INTERVAL = 1.9

ANIMATION_SPEED = 0.12
ANIMATION_FRAME_COUNT = 3

MAX_UP_ANGLE = 35
MAX_DOWN_ANGLE = -70
ANGLE_LERP_SPEED = 8.0

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.load_settings()
        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.load_player_animation()

        self.day_background = None
        self.night_background = None
        try:
            self.day_background = arcade.load_texture("assets/background-day.png")
            self.night_background = arcade.load_texture("assets/background-night.png")
        except Exception as e:
            print("Ошибка загрузки фона:", e)

        self.pipe_texture = None
        try:
            self.pipe_texture = arcade.load_texture("assets/pipe-green.png")
        except Exception as e:
            print("Ошибка загрузки текстуры трубы:", e)

        self.background_list = arcade.SpriteList()
        self.background_sprite = arcade.Sprite()
        self.background_sprite.center_x = self.window.width / 2
        self.background_sprite.center_y = self.window.height / 2
        self.background_sprite.width = self.window.width
        self.background_sprite.height = self.window.height
        self.background_sprite.texture = self.day_background
        self.background_list.append(self.background_sprite)

        self.current_background_is_day = True

        self.player = arcade.Sprite(scale=0.15)
        self.player.center_x = 250
        self.player.center_y = self.window.height // 2
        self.player.velocity_y = 0
        self.player.texture = self.animation_textures[0]
        self.player.angle = 0

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.current_frame = 0
        self.animation_timer = 0.0

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

    def load_player_animation(self):
        base_names = {
            "bird": "classic",
            "plane": "plane",
            "robot": "robot"
        }
        skin_base = base_names.get(self.skin, "robot")

        self.animation_textures = []
        success = True
        for i in range(1, ANIMATION_FRAME_COUNT + 1):
            try:
                filename = f"assets/{skin_base}{i}.png"
                texture = arcade.load_texture(filename)
                self.animation_textures.append(texture)
            except:
                success = False
                break

        if not success or len(self.animation_textures) != ANIMATION_FRAME_COUNT:
            fallback = arcade.load_texture(":resources:images/animated_characters/robot/robot_idle.png")
            self.animation_textures = [fallback] * ANIMATION_FRAME_COUNT

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
        self.difficulty = diff

        if diff == "easy":
            self.pipe_interval = 2.5
            self.pipe_gap = 240
        elif diff == "medium":
            self.pipe_interval = BASE_PIPE_INTERVAL
            self.pipe_gap = 220
        else:
            self.pipe_interval = 1.5
            self.pipe_gap = 180

        self.volume = settings.get("volume", 80)
        self.skin = settings.get("skin", "robot")

    def setup(self):
        self.player.center_y = self.window.height // 2
        self.player.velocity_y = 0
        self.player.angle = 0
        self.score = 0
        self.score_text.text = "0"
        self.pipe_list.clear()
        self.last_pipe_time = 0.0
        self.last_update_time = 0.0
        self.game_started = False
        self.game_over = False
        self.current_frame = 0
        self.animation_timer = 0.0
        self.player.texture = self.animation_textures[0]
        self.current_background_is_day = True
        self.background_sprite.texture = self.day_background

    def on_show_view(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_update(self, delta_time: float):
        if not self.game_started or self.game_over:
            return

        self.player.velocity_y -= self.gravity
        self.player.center_y += self.player.velocity_y

        if self.player.velocity_y > 0:
            target_angle = -35
        else:
            fall_factor = min(1.0, abs(self.player.velocity_y) / 12.0)
            target_angle = 70 * fall_factor

        self.player.angle += (target_angle - self.player.angle) * ANGLE_LERP_SPEED * delta_time
        self.player.angle = max(-90, min(45, self.player.angle))

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

            if self.score % 10 == 0 and self.score > 0:
                if self.current_background_is_day:
                    self.current_background_is_day = False
                    self.background_sprite.texture = self.night_background
                else:
                    self.current_background_is_day = True
                    self.background_sprite.texture = self.day_background

        self.last_update_time += delta_time
        if self.last_update_time - self.last_pipe_time > self.pipe_interval:
            self.spawn_pipe()
            self.last_pipe_time = self.last_update_time

        self.animation_timer += delta_time
        if self.animation_timer >= ANIMATION_SPEED:
            self.animation_timer -= ANIMATION_SPEED
            self.current_frame = (self.current_frame + 1) % ANIMATION_FRAME_COUNT
            self.player.texture = self.animation_textures[self.current_frame]

        self.check_collisions()

    def spawn_pipe(self):
        min_y = 140
        max_y = self.window.height - 140 - self.pipe_gap

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

        bottom_height = gap_y
        top_height = self.window.height - (gap_y + self.pipe_gap)

        bottom_pipe = arcade.Sprite()
        if self.pipe_texture:
            bottom_pipe.texture = self.pipe_texture
        bottom_pipe.width = BASE_PIPE_WIDTH
        bottom_pipe.height = bottom_height
        bottom_pipe.center_x = self.window.width + 200
        bottom_pipe.bottom = 0
        bottom_pipe.center_y = bottom_height / 2

        top_pipe = arcade.Sprite()
        if self.pipe_texture:
            top_pipe.texture = self.pipe_texture
            top_pipe.angle = 180
        top_pipe.width = BASE_PIPE_WIDTH
        top_pipe.height = top_height
        top_pipe.center_x = self.window.width + 200
        top_pipe.top = self.window.height
        top_pipe.center_y = self.window.height - top_height / 2

        self.pipe_list.append(top_pipe)
        self.pipe_list.append(bottom_pipe)

        self.last_gap_y = gap_y

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

        self.background_list.draw()

        if self.game_started and not self.game_over:
            self.pipe_list.draw()

        self.player_list.draw()

        self.score_text.draw()

        if not self.game_started:
            self.ready_text.draw()

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
