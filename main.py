# main.py

import logging
from modules.telegram_bot import main as start_telegram_bot

def setup_logging():
    """Настройка логирования для проекта."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/bot.log"),
            logging.StreamHandler()
        ]
    )
    logging.info("Логирование успешно настроено.")

if __name__ == "__main__":
    setup_logging()
    logging.info("Запуск Telegram-бота...")
    start_telegram_bot()
