from dotenv import load_dotenv
import os

# Загрузка переменных из .env
load_dotenv()

# Токен Telegram-бота
TOKEN = os.getenv("TOKEN")

# Список администраторов (целые числа через запятую)
ADMIN_ID = list(map(int, os.getenv("ADMIN_ID", "").split(",")))

# Токен платежной системы
PAYMASTER = os.getenv("PAYMASTER")
