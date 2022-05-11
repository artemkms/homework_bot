import logging
import os
import time

import requests
from requests.exceptions import RequestException
import telegram
from dotenv import load_dotenv

from exception import ResponsePracticumException

load_dotenv()

PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def send_message(bot, message):
    """Отправка сообщения в чат."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except telegram.error.TelegramError as e:
        logger.critical(f"Не удалось отправить сообщение - {e}")
    else:
        logger.info(f"Бот отправил сообщение: {message}")


def get_api_answer(current_timestamp):
    """Запрос к эндпоинту API-сервиса."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except RequestException as err:
        raise ResponsePracticumException(err)
    if response.status_code != 200:
        error_description = f"Ошибка, Код ответа: {response.status_code}"
        raise ResponsePracticumException(error_description)
    return response.json()


def check_response(response):
    """Проверка ответа API на корректность."""
    if not isinstance(response, dict):
        err = "Неверный тип данных у элемента response"
        raise TypeError(err)
    elif "homeworks" not in response:
        err = "В ответе от API отсутствует ключ homeworks"
        raise ResponsePracticumException(err)
    elif not isinstance(response["homeworks"], list):
        err = "Неверный тип данных у элемента homeworks"
        raise ResponsePracticumException(err)
    return response.get("homeworks")


def parse_status(homework):
    """Извлечение статуса работы."""
    homework_name = homework["homework_name"]
    homework_status = homework["status"]
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверка доступности переменных окружения."""
    if (
        PRACTICUM_TOKEN is None
        or TELEGRAM_TOKEN is None
        or TELEGRAM_CHAT_ID is None
    ):
        logger.critical("Отсутствие обязательных переменных окружения!")
        return False
    return True


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    last_error = ""
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if len(homeworks) > 0:
                current_homework = homeworks[0]
                lesson_name = current_homework["lesson_name"]
                hw_status = parse_status(current_homework)
                send_message(bot, f"{lesson_name}. {hw_status}")
            else:
                logger.debug("Новые статусы отсутствуют.")
            current_timestamp = response.get("current_date")
            last_error = ""
        except Exception as err:
            message = f"Сбой в работе программы: {err}"
            if str(err) != str(last_error):
                send_message(bot, message)
                last_error = err
            logger.error(message)
        time.sleep(RETRY_TIME)


if __name__ == '__main__':
    if check_tokens():
        main()
    else:
        SystemExit()
