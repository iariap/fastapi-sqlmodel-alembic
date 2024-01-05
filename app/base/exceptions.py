from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import NoResultFound


def add_exceptions_handlers(app: FastAPI):
    @app.exception_handler(NoResultFound)
    def handle_NoResultFound(request: Request, exc: NoResultFound):
        return JSONResponse(
            status_code=404,
            content={"message": "Not found"},
        )
