from fastapi import FastAPI
from fastapi_pagination import add_pagination


from base.db import init_db
from base.exceptions import add_exceptions_handlers
from songs.routes import router as songs_router

app = FastAPI()


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.post("/initdb")
async def init_db_route() -> None:
    await init_db()


app.include_router(songs_router)

add_pagination(app)
add_exceptions_handlers(app)
