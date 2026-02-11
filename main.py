import arcade
from mainmenu import MenuView
from gamescreen import GameView
import sqlite3


def init_database():
    conn = sqlite3.connect("game.db")
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            difficulty TEXT DEFAULT 'medium',          -- ← добавлен
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS settings_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            skin TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


# Вызови один раз при запуске
init_database()
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
