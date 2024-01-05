from fastapi import APIRouter
from fastapi_pagination import LimitOffsetPage
from pydantic import BaseModel

from base.crud import GenericCRUD
from base.db import DBSession


class GenericCrudRouter(APIRouter):
    def __init__(
        self,
        model_type: BaseModel,
        GetSchemaType: BaseModel,
        CreateSchemaType: BaseModel,
        UpdateSchemaType: BaseModel,
    ):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        obj_name = f"{model_type.__name__.lower()}s"
        super().__init__(prefix=f"/{obj_name}", tags=[obj_name.capitalize()])
        self.crud = GenericCRUD(model_type)

        @self.get("", name=f"Gets all {model_type.__name__.capitalize()}s")
        async def get_all(
            db: DBSession,
        ) -> LimitOffsetPage[GetSchemaType]:
            return await self.crud.paginate(db)

        @self.get(
            "/{id}",
            name=f"Gets an existing {model_type.__name__.lower()} by id",
        )
        async def get_by_id(
            id: str,
            db: DBSession,
        ) -> GetSchemaType:
            return await self.crud.get(db, id)

        @self.post("", name=f"Creates a new {model_type.__name__.lower()}")
        async def create(
            obj_in: CreateSchemaType,
            db: DBSession,
        ) -> GetSchemaType:
            return await self.crud.create(db, obj_in=obj_in)

        @self.put(
            "/{id}", name=f"Updates an existing {model_type.__name__.lower()}"
        )
        async def update(
            id: str,
            obj_in: UpdateSchemaType,
            db: DBSession,
        ) -> GetSchemaType:
            obj = await self.crud.get(db, id)
            return await self.crud.update(db, db_obj=obj, obj_in=obj_in)

        @self.delete(
            "/{id}",
            status_code=203,
            name=f"Deletes the {model_type.__name__.lower()} by id",
        )
        async def delete(
            id: str,
            db: DBSession,
        ):
            await self.crud.remove(db, id=id)
            return None
