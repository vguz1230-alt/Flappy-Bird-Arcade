import sys
import logging
from PyQt6.QtWidgets import QApplication
from app_controller import AppController

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting application")

    # 1. Создаем QApplication (обязательно в начале)
    app = QApplication(sys.argv)

    try:
        # 2. Передаем app в контроллер
        controller = AppController(app)

        # 3. Запуск приложения (главный цикл)
        sys.exit(app.exec())

    except Exception as e:
        logger.critical(f"Fatal error during application startup: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
