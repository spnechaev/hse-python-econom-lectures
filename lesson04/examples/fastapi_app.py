"""A minimal FastAPI application."""

from fastapi import FastAPI


app = FastAPI()


@app.get("/hello")
def hello(name: str = "world") -> dict[str, str]:
    return {"message": f"Hello, {name}!"}
