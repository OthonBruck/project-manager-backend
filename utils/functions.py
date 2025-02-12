from typing import Type, TypeVar, Callable, List
from fastapi import Depends, HTTPException, status
from db.database import get_database
from bson.objectid import ObjectId

T = TypeVar("T")

def serialize_document(document: dict) -> dict:
    if document and "_id" in document:
        document["id"] = str(document["_id"])
        del document["_id"]
    if document and "created_at" in document:
        document["created_at"] = document["created_at"].isoformat()
    if document and "updated_at" in document:
        document["updated_at"] = document["updated_at"].isoformat()
    return document

def serialize_list(documents: list) -> list:
    return [serialize_document(doc) for doc in documents]


async def check_permission(
    project_id: str,
    required_roles: List[str],
    current_user: dict,
    db=get_database()
):
    project = await db.get_collection("project").find_one({"_id": ObjectId(project_id)})
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    user_role = next(
        (member["role"] for member in project.get("members", []) if member["user_id"] == current_user),
        None
    )
    if project.get("owner", "") != current_user and (not user_role or user_role not in required_roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission not granted")

    return project
