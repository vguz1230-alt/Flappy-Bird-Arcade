import arcade
import random

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GRAVITY = 0.4
JUMP_POWER = 9
PIPE_SPEED = 3.8
PIPE_GAP = 180
PIPE_WIDTH = 90
PIPE_INTERVAL = 1.9

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.player = arcade.Sprite(
            ":resources:images/animated_characters/robot/robot_idle.png",
            scale=0.6
        )
        self.player.center_x = 250
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player.velocity_y = 0

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.pipe_list = arcade.SpriteList()

        self.last_pipe_time = 0
        self.last_update_time = 0.0

        self.score = 0
        self.score_text = arcade.Text(
            "0",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 80,
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
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            arcade.color.WHITE,
            40,
            font_name="Arial",
            anchor_x="center",
            anchor_y="center"
        )

        self.game_over_text = arcade.Text(
            "ИГРА ОКОНЧЕНА",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 80,
            arcade.color.RED,
            60,
            font_name="Kenney Future",
            anchor_x="center",
            anchor_y="center"
        )

        self.final_score_text = arcade.Text(
            "",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            arcade.color.WHITE,
            48,
            font_name="Arial",
            anchor_x="center",
            anchor_y="center"
        )

    def setup(self):
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player.velocity_y = 0
        self.score = 0
        self.score_text.text = "0"
        self.pipe_list.clear()
        self.last_pipe_time = 0
        self.last_update_time = 0.0
        self.game_started = False
        self.game_over = False

    def on_show_view(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_update(self, delta_time: float):
        if not self.game_started or self.game_over:
            return

        self.player.velocity_y -= GRAVITY
        self.player.center_y += self.player.velocity_y

        if self.player.top < 0 or self.player.bottom > SCREEN_HEIGHT:
            self.game_over = True
            self.final_score_text.text = f"Счёт: {self.score}"
            return

        # Двигаем все трубы вручную
        for pipe in self.pipe_list:
            pipe.center_x -= PIPE_SPEED

        # Удаляем пары труб, которые ушли за левый край
        while len(self.pipe_list) >= 2 and self.pipe_list[0].right < 0:
            self.pipe_list.pop(0)
            self.pipe_list.pop(0)
            self.score += 1
            self.score_text.text = str(self.score)

        # Генерация новых труб
        self.last_update_time += delta_time
        if self.last_update_time - self.last_pipe_time > PIPE_INTERVAL:
            self.spawn_pipe()
            self.last_pipe_time = self.last_update_time

        self.check_collisions()

    def spawn_pipe(self):
        gap_y = random.randint(140, SCREEN_HEIGHT - 140 - PIPE_GAP)

        top_pipe = arcade.SpriteSolidColor(PIPE_WIDTH, SCREEN_HEIGHT, arcade.color.FOREST_GREEN)
        top_pipe.center_x = SCREEN_WIDTH + 200
        top_pipe.bottom = gap_y + PIPE_GAP

        bottom_pipe = arcade.SpriteSolidColor(PIPE_WIDTH, SCREEN_HEIGHT, arcade.color.FOREST_GREEN)
        bottom_pipe.center_x = SCREEN_WIDTH + 200
        bottom_pipe.top = gap_y

        self.pipe_list.append(top_pipe)
        self.pipe_list.append(bottom_pipe)

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
            self.player.velocity_y = JUMP_POWER

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.game_over:
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.setup()
            return

        if not self.game_started:
            self.game_started = True
            return

        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player.velocity_y = JUMP_POWER

    def on_draw(self):
        self.clear()

        if self.game_started and not self.game_over:
            self.pipe_list.draw()

        self.player_list.draw()

        self.score_text.draw()

        if not self.game_started:
            self.ready_text.draw()

        if self.game_over:
            arcade.draw_lbwh_rectangle_filled(
                0, 0,
                SCREEN_WIDTH, SCREEN_HEIGHT,
                (0, 0, 0, 140)
            )
            self.game_over_text.draw()
            self.final_score_text.draw()

            arcade.draw_text(
                "ЛКМ — Перезапустить",
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60,
                arcade.color.WHITE, 28, anchor_x="center"
            )
            arcade.draw_text(
                "ESC / ENTER — В меню",
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100,
                arcade.color.WHITE, 28, anchor_x="center"
            )