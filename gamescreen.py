import arcade
import random
import json
import sqlite3
import datetime

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

        self.background_sprite = arcade.Sprite()
        self.background_sprite.center_x = self.window.width / 2
        self.background_sprite.center_y = self.window.height / 2
        self.background_sprite.width = self.window.width
        self.background_sprite.height = self.window.height

        self.update_background_texture()

        self.background_list = arcade.SpriteList()
        self.background_list.append(self.background_sprite)

        self.pipe_texture = None
        try:
            self.pipe_texture = arcade.load_texture("assets/pipe-green.png")
        except Exception as e:
            print("Ошибка загрузки текстуры трубы:", e)

        try:
            self.sound_wing = arcade.load_sound("assets/audio_wing.wav")
            self.sound_point = arcade.load_sound("assets/audio_point.wav")
            self.sound_hit = arcade.load_sound("assets/audio_hit.wav")
        except Exception as e:
            print("Ошибка загрузки звуков:", e)
            self.sound_wing = None
            self.sound_point = None
            self.sound_hit = None

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

        self.player_name_text = arcade.Text(
            self.player_name,
            40,
            self.window.height - 60,
            arcade.color.WHITE,
            32,
            font_name="Arial",
            anchor_x="left",
            anchor_y="center"
        )

        difficulty_ru = {
            "easy": "Легко",
            "medium": "Средне",
            "hard": "Сложно"
        }.get(self.difficulty, self.difficulty.capitalize())

        self.difficulty_text = arcade.Text(
            f"Сложность: {difficulty_ru}",
            self.window.width - 40,
            self.window.height - 40,
            arcade.color.RED,
            24,
            font_name="Arial",
            anchor_x="right",
            anchor_y="center"
        )

        self.best_score = self.load_best_score()
        self.best_score_text = arcade.Text(
            f"Рекорд: {self.best_score}" if self.best_score is not None else "",
            self.window.width - 40,
            self.window.height - 75,
            arcade.color.YELLOW,
            28,
            font_name="Arial",
            anchor_x="right",
            anchor_y="center"
        )

        self.particles = []

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

    def update_background_texture(self):
        try:
            if self.easter_mode:
                tex = arcade.load_texture("assets/easter_day.png")
            else:
                tex = arcade.load_texture("assets/background-day.png")
            self.background_sprite.texture = tex
            self.current_background_is_day = True
        except Exception as e:
            print("Ошибка загрузки фона:", e)

    def load_player_animation(self):
        if self.easter_mode:
            try:
                texture = arcade.load_texture("assets/easter_egg.png")
                self.animation_textures = [texture] * ANIMATION_FRAME_COUNT
            except:
                fallback = arcade.load_texture(":resources:images/animated_characters/robot/robot_idle.png")
                self.animation_textures = [fallback] * ANIMATION_FRAME_COUNT
            return

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
                "skin": "robot",
                "player_name": "Игрок"
            }

        self.player_name = settings.get("player_name", "Игрок").strip()
        self.easter_mode = (self.player_name.lower() == "дима петухов")

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

        if not self.easter_mode:
            self.skin = settings.get("skin", "robot")
        else:
            self.skin = "easter_egg"

    def load_best_score(self):
        conn = sqlite3.connect("game.db")
        c = conn.cursor()
        c.execute("SELECT MAX(score) FROM games WHERE player_name = ? AND difficulty = ?",
                  (self.player_name, self.difficulty))
        result = c.fetchone()[0]
        conn.close()
        return result

    def save_game_result(self):
        conn = sqlite3.connect("game.db")
        c = conn.cursor()
        date_str = datetime.datetime.now().isoformat()
        c.execute("INSERT INTO games (player_name, score, difficulty) VALUES (?, ?, ?)",
                  (self.player_name, self.score, self.difficulty))
        c.execute("INSERT INTO settings_history (player_name, difficulty, skin, date) VALUES (?, ?, ?, ?)",
                  (self.player_name, self.difficulty, self.skin, date_str))
        conn.commit()
        conn.close()

    def create_explosion(self):
        colors = [arcade.color.RED, arcade.color.ORANGE, arcade.color.YELLOW, arcade.color.WHITE]
        for _ in range(60):
            particle = {
                'x': self.player.center_x,
                'y': self.player.center_y,
                'dx': random.uniform(-6, 6),
                'dy': random.uniform(-6, 6),
                'size': random.uniform(4, 12),
                'color': random.choice(colors),
                'alpha': 255,
                'life': random.uniform(0.6, 1.2)
            }
            self.particles.append(particle)

    def create_click_particles(self, x, y):
        colors = [
            arcade.color.WHITE,
            arcade.color.LIGHT_BLUE,
            arcade.color.LIGHT_CYAN,
            arcade.color.LIGHT_GREEN,
            arcade.color.LIGHT_YELLOW
        ]
        for _ in range(18):
            particle = {
                'x': x,
                'y': y,
                'dx': random.uniform(-3.5, 3.5),
                'dy': random.uniform(5, 12),
                'size': random.uniform(3, 9),
                'color': random.choice(colors),
                'alpha': 255,
                'life': random.uniform(0.7, 1.4)
            }
            self.particles.append(particle)

    def update_particles(self, delta_time):
        new_particles = []
        for p in self.particles:
            p['x'] += p['dx'] * 60 * delta_time
            p['y'] += p['dy'] * 60 * delta_time
            p['dy'] -= 18 * delta_time
            p['life'] -= delta_time
            p['alpha'] = int(255 * max(0, p['life'] / 1.4))
            if p['life'] > 0:
                new_particles.append(p)
        self.particles = new_particles

    def draw_particles(self):
        for p in self.particles:
            arcade.draw_circle_filled(
                p['x'], p['y'],
                p['size'],
                (*p['color'][:3], p['alpha'])
            )

    def setup(self):
        self.player.center_y = self.window.height // 2
        self.player.velocity_y = 0
        self.player.angle = 0
        self.score = 0
        self.score_text.text = "0"
        self.player_name_text.text = self.player_name
        self.pipe_list.clear()
        self.last_pipe_time = 0.0
        self.last_update_time = 0.0
        self.game_started = False
        self.game_over = False
        self.current_frame = 0
        self.animation_timer = 0.0
        self.player.texture = self.animation_textures[0]
        self.player.visible = True

        self.background_sprite.center_x = self.window.width / 2
        self.background_sprite.center_y = self.window.height / 2
        self.background_sprite.width = self.window.width
        self.background_sprite.height = self.window.height
        self.update_background_texture()

        self.player_name_text.y = self.window.height - 60

        self.best_score = self.load_best_score()
        self.best_score_text.text = f"Рекорд: {self.best_score}" if self.best_score is not None else ""

        self.particles = []

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)

        self.background_sprite.width = width
        self.background_sprite.height = height
        self.background_sprite.center_x = width / 2
        self.background_sprite.center_y = height / 2

        self.score_text.x = width // 2
        self.score_text.y = height - 80

        self.ready_text.x = width // 2
        self.ready_text.y = height // 2

        self.game_over_text.x = width // 2
        self.game_over_text.y = height // 2 + 80

        self.final_score_text.x = width // 2
        self.final_score_text.y = height // 2

        self.player_name_text.y = height - 60

        self.difficulty_text.x = width - 40
        self.difficulty_text.y = height - 40

        self.best_score_text.x = width - 40
        self.best_score_text.y = height - 75

    def on_update(self, delta_time: float):
        self.update_particles(delta_time)

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
            if self.sound_hit:
                arcade.play_sound(self.sound_hit, volume=self.volume / 100)
            self.create_explosion()
            self.player.visible = False
            self.save_game_result()
            return

        for pipe in self.pipe_list:
            pipe.center_x -= BASE_PIPE_SPEED

        while len(self.pipe_list) >= 2 and self.pipe_list[0].right < 0:
            self.pipe_list.pop(0)
            self.pipe_list.pop(0)
            self.score += 1
            self.score_text.text = str(self.score)
            if self.sound_point:
                arcade.play_sound(self.sound_point, volume=self.volume / 100)

            if self.score % 10 == 0 and self.score > 0:
                if self.current_background_is_day:
                    self.current_background_is_day = False
                    try:
                        if self.easter_mode:
                            tex = arcade.load_texture("assets/easter_night.png")
                        else:
                            tex = arcade.load_texture("assets/background-night.png")
                        self.background_sprite.texture = tex
                    except Exception as e:
                        print("Ошибка смены ночного фона:", e)
                else:
                    self.current_background_is_day = True
                    self.update_background_texture()

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
                if self.sound_hit:
                    arcade.play_sound(self.sound_hit, volume=self.volume / 100)
                self.create_explosion()
                self.player.visible = False
                self.save_game_result()
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
            if self.sound_wing:
                arcade.play_sound(self.sound_wing, volume=self.volume / 100)

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
            if self.sound_wing:
                arcade.play_sound(self.sound_wing, volume=self.volume / 100)
            self.create_click_particles(x, y)

    def on_draw(self):
        self.clear()

        self.background_list.draw()

        if self.game_started and not self.game_over:
            self.pipe_list.draw()

        self.player_list.draw()

        self.draw_particles()

        self.score_text.draw()
        self.player_name_text.draw()
        self.difficulty_text.draw()
        self.best_score_text.draw()

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