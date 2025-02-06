from typing import Type, TypeVar, Callable
from fastapi import Depends
from db.database import get_database

T = TypeVar("T")

def serialize_document(document: dict) -> dict:
    if document and "_id" in document:
        document["id"] = str(document["_id"])
        del document["_id"]
    if document and "created_at" in document:
        document["created_at"] = document["created_at"].isoformat()
    return document

def serialize_list(documents: list) -> list:
    return [serialize_document(doc) for doc in documents]

def get_service(service_class: Type[T]) -> Callable:
    def _get_service(db=Depends(get_database)) -> T:
        return service_class(db)
    return _get_service