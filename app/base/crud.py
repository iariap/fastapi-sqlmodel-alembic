from datetime import datetime
from typing import Any, Dict, Type

from fastapi.encoders import jsonable_encoder
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate as fap_paginate
from pydantic import BaseModel
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.base.models import SoftDeleteModel


class GenericCRUD[
    ModelType: BaseModel,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
]:
    def __init__(self, model_type: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model_type = model_type

    def apply_soft_delete_filtering(self, statement):
        """If the model is soft delete, then filter out the deleted items"""
        if issubclass(self.model_type, SoftDeleteModel):
            statement = statement.filter(self.model_type.deleted_at == None)
        return statement

    async def get(self, db: AsyncSession, id: Any) -> ModelType:
        statement = select(self.model_type).filter(self.model_type.id == id)
        statement = self.apply_soft_delete_filtering(statement)

        result = await db.exec(statement)
        answer = result.one()
        return answer

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model_type(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        id: Any,
        obj_in: UpdateSchemaType | Dict[str, Any],
    ) -> ModelType:
        db_obj = await self.get(db, id)
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        obj = await self.get(db, id)

        if issubclass(self.model_type, SoftDeleteModel):
            obj.deleted_at = datetime.utcnow()
        else:
            await db.delete(obj)
        await db.commit()
        return obj

    async def paginate(self, db: AsyncSession) -> LimitOffsetPage[ModelType]:
        statement = select(self.model_type).order_by(self.model_type.id)

        statement = self.apply_soft_delete_filtering(statement)

        return await fap_paginate(
            db,
            statement,
            subquery_count=False,
        )

    async def get_all(self, db: AsyncSession) -> list[ModelType]:
        statement = select(self.model_type).order_by(self.model_type.id)

        statement = self.apply_soft_delete_filtering(statement)

        result = await db.exec(statement)
        return result.all()
