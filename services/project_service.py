from schemas.project import ProjectCreate
from fastapi import HTTPException
from bson.objectid import ObjectId
from utils.functions import serialize_document

class ProjectService:
    def __init__(self, db):
        self.db = db
    
    async def create_project(self, project_data: ProjectCreate, current_user):
        new_project = {
            "title": project_data.title,
            "description": project_data.description,
            "owner": current_user,
            "members": []
        }
        await self.db.get_collection("project").insert_one(new_project)

        return new_project

    async def get_project_by_id(self, id):
        result = await self.db.get_collection("project").find_one({"_id": ObjectId(id)})
        if not result:
            raise HTTPException(status_code=400, detail="Project does not exist.")
        return serialize_document(result)
    
    async def add_member_to_project(self,project_id, member, current_user):
        project = await self.db.get_collection("project").find_one({"_id": ObjectId(project_id)})
        if not project:
            raise HTTPException(status_code=400, detail="Project does not exist.")
        
        if member in project["members"]:
            raise HTTPException(status_code=400, detail="User is already a member")
        
        await self.db.get_collection("project").update_one({"_id": ObjectId(project_id)}, {"$push": {"members": member.user_id}})

        return {"message": "User added to project"}
