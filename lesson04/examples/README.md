# Минимальные приложения к лекции 04

Каждый файл — самостоятельный запускаемый пример. Создайте отдельное окружение и установите зависимости:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r lesson04/examples/requirements.txt
```

## CSV-отчёт

```bash
python lesson04/examples/csv_report.py lesson04/examples/sales.csv
```

## Линейная регрессия

```bash
python lesson04/examples/linear_regression.py
```

## FastAPI

```bash
cd lesson04/examples
uvicorn fastapi_app:app --reload
```

Откройте <http://127.0.0.1:8000/hello?name=Student> и <http://127.0.0.1:8000/docs>.

## Telegram echo-bot

Создайте бота через BotFather и передайте токен через переменную окружения:

```bash
export TELEGRAM_BOT_TOKEN="..."
python lesson04/examples/telegram_echo_bot.py
```

Токен нельзя добавлять в код, notebook, README или Git.

## Pygame

```bash
python lesson04/examples/pygame_ball.py
```

Закройте окно обычной кнопкой закрытия.
