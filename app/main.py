import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.base.exceptions import add_exceptions_handlers
from app.config import settings
from app.songs.routes import router as songs_router
from app.tooling import router as tooling_router

app = FastAPI(openapi_url=settings.OPENAPI_URL)


app.include_router(songs_router)
app.include_router(tooling_router)

add_pagination(app)
add_exceptions_handlers(app)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, workers=3)
