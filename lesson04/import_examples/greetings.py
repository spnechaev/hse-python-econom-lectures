"""A small module that makes its first import visible."""

print("greetings: выполняется код модуля")

PREFIX = "Привет"


def greet(name: str) -> str:
    return f"{PREFIX}, {name}!"


if __name__ == "__main__":
    print(greet("Саша"))
