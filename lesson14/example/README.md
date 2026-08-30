# Минимальный FastAPI-проект

Пример показывает один сквозной сценарий: создать задачу, увидеть список и отметить задачу выполненной. Данные хранятся в памяти и исчезают после перезапуска — это сознательная граница примера, а не production-хранилище.

Каталог можно рассматривать как корень отдельного маленького репозитория. Если пример остаётся внутри репозитория курса, вложенный `.github/workflows/ci.yml` служит образцом и не запускается GitHub автоматически: рабочие workflow GitHub читает из `.github/workflows` в корне репозитория.

## Локальный запуск

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
fastapi dev app/main.py
```

Откройте <http://127.0.0.1:8000/docs> и <http://127.0.0.1:8000/health>.

## Проверка

```bash
ruff check .
pytest
```

## Контейнер

```bash
docker build -t course-task-api .
docker run --rm -p 8000:8000 -e APP_NAME="My Task API" course-task-api
```

Либо:

```bash
docker compose up --build
docker compose ps
docker compose down
```

В image не копируются тесты, Git и локальное окружение. Секретные значения в Compose-файл и Dockerfile добавлять нельзя.
