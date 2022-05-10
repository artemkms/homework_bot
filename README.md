# Бот-ассистент
[![Python](https://img.shields.io/badge/Made%20with-Python-green?logo=python&logoColor=white&color)](https://www.python.org/)
[![Telegram](https://img.shields.io/static/v1?message=bot&logo=telegram&labelColor=5c5c5c&color=1182c3&logoColor=white&label=%20&style=plastic)](https://core.telegram.org/bots/api)
[![Pyrogram](https://img.shields.io/static/v1?message=pyrogram&logo=github&labelColor=5c5c5c&color=1182c3&logoColor=white&label=%20&style=plastic)](https://github.com/pyrogram/pyrogram)


## О проекте:
**Telegram-бот, который обращается к API сервиса `Практикум.Домашка` и узнает статус домашней работы: взята ли в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.**

### Что делает бот:
- раз в 10 минут опрашивает API сервиса Практикум.Домашка и проверяет статус отправленной на ревью домашней работы;
- при обновлении статуса анализирует ответ API и отправляет соответствующее уведомление в Telegram;
- логирет свою работу и сообщает о важных проблемах сообщением в Telegram.

### Запуск проекта:
Клонировать репозиторий и перейти в него в командной строке:
```sh
git clone git@github.com:artemkms/homework_bot.git
```
Скопировать `.env.example` и назвать его `.env`:
```sh
cp .env.example .env
```
Заполнить переменные окружения в `.env`:
```sh
PRACTICUM_TOKEN = токен_к_api_практикум.домашка
TELEGRAM_TOKEN = токен_вашего_тг_бота
TELEGRAM_CHAT_ID = ваш_telegram_ID
```
Установить и активировать виртуальное окружение:
```sh
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt
```sh
pip install -r requirements.txt
```
В папке с файлом homework.py выполните команду:
```sh
python homework.py
```

### Логика работы бота:
1. `check_tokens()` - проверяет доступность переменных окружения. Должны присутствовать все переменные окружения;
2. `get_api_answer()` - запрос к эндпоинту API-сервиса. В случае успешного запроса возвращается ответ API, преобразованный из формата JSON к типам данных Python;
3. `check_response()` -  проверка ответа API на корректность. Если ответ API соответствует ожиданиям, то функция возвращает список домашних работ (он может быть и пустым), доступный в ответе API по ключу `homeworks`;
4. `parse_status()` - извлекает из информации о конкретной домашней работе статус этой работы. В случае успеха, функция возвращает подготовленную для отправки в Telegram строку, содержащую один из вердиктов словаря HOMEWORK_STATUSES;
5. `send_message()` - отправляет сообщение в Telegram чат, определяемый переменной окружения TELEGRAM_CHAT_ID.

### Логирование:
Каждое сообщение в журнале логов состоит как минимум из:
- даты и времени события;
- уровня важности события;
- описания события. 

**Примеры:**
```sh
2022-05-09 15:34:45,150 [ERROR] Сбой в работе программы: Эндпоинт https://practicum.yandex.ru/api/user_api/homework_statuses/111 недоступен. Код ответа API: 404
2022-05-09 15:34:45,355 [INFO] Бот отправил сообщение "Сбой в работе программы: Эндпоинт [https://practicum.yandex.ru/api/user_api/homework_statuses/](https://practicum.yandex.ru/api/user_api/homework_statuses/) недоступен. Код ответа API: 404"
2022-05-09 16:19:13,149 [CRITICAL] Отсутствует обязательная переменная окружения: 'TELEGRAM_CHAT_ID'
Программа принудительно остановлена.
```

**Обязательно логируются события:**
- отсутствие обязательных переменных окружения во время запуска бота (уровень `CRITICAL`).
- удачная отправка любого сообщения в Telegram (уровень `INFO`);
- сбой при отправке сообщения в Telegram (уровень `ERROR`);
- недоступность эндпоинта https://practicum.yandex.ru/api/user_api/homework_statuses/ (уровень `ERROR`);
- любые другие сбои при запросе к эндпоинту (уровень `ERROR`);
- отсутствие ожидаемых ключей в ответе API (уровень `ERROR`);
- недокументированный статус домашней работы, обнаруженный в ответе API (уровень `ERROR`);
- отсутствие в ответе новых статусов (уровень `DEBUG`).

События уровня `ERROR` не только логируются, но и пересылается информация о них в Telegram в тех случаях, когда это технически возможно.

#### Краткая документация к API-сервису и примеры запросов доступны по [ссылке](https://code.s3.yandex.net/backend-developer/learning-materials/delugov/%D0%9F%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D1%83%D0%BC.%D0%94%D0%BE%D0%BC%D0%B0%D1%88%D0%BA%D0%B0%20%D0%A8%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0.pdf).





