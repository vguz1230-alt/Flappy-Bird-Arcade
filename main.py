import arcade
from mainmenu import MenuView
from gamescreen import GameView

SCREEN_TITLE = "Flappy Bird"

def main():
    window = arcade.Window(
        title=SCREEN_TITLE,
        fullscreen=True,
        resizable=False,
        visible=True
    )

    SCREEN_WIDTH = window.width
    SCREEN_HEIGHT = window.height

    menu_view = MenuView()
    game_view = GameView()

    window.menu_view = menu_view

    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()