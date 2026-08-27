"""A minimal Telegram echo-bot using the HTTP Bot API directly."""

from __future__ import annotations

import os

import requests


TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


def send_message(chat_id: int, text: str) -> None:
    response = requests.post(
        f"{BASE_URL}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=10,
    )
    response.raise_for_status()


def main() -> None:
    offset: int | None = None

    while True:
        response = requests.get(
            f"{BASE_URL}/getUpdates",
            params={"timeout": 30, "offset": offset},
            timeout=35,
        )
        response.raise_for_status()

        for update in response.json()["result"]:
            offset = update["update_id"] + 1
            message = update.get("message")
            if message is None or "text" not in message:
                continue

            chat_id = message["chat"]["id"]
            send_message(chat_id, f"Вы написали: {message['text']}")


if __name__ == "__main__":
    main()
