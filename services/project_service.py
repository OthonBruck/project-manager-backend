from schemas.project import ProjectCreate
from fastapi import HTTPException
from bson.objectid import ObjectId
from utils.functions import serialize_document

class ProjectService:
    @staticmethod
    async def create_project(project_data: ProjectCreate, db):
        new_project = {
            "title": project_data.title,
            "description": project_data.description,
        }
        await db.get_collection("project").insert_one(new_project)

        return new_project

    async def get_project_by_id(id, db):
        result = await db.get_collection("project").find_one({"_id": ObjectId(id)})
        if not result:
            raise HTTPException(status_code=400, detail="Project does not exist.")
        return serialize_document(result)