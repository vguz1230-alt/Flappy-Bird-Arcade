import arcade
from mainmenu import MenuView
from gamescreen import GameView

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Flappy Bird"

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)

    menu_view = MenuView()
    game_view = GameView()

    # Сохраняем ссылку на меню для возврата из игры
    window.menu_view = menu_view

    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
