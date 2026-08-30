FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN python -m pip install --no-cache-dir -r /code/requirements.txt

COPY app /code/app

EXPOSE 8000
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
