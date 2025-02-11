from schemas.project import ProjectCreate
from fastapi import HTTPException
from bson.objectid import ObjectId
from utils.functions import serialize_document, check_permission, serialize_list
from services.websocket_service import send_notification

class ProjectService:
    def __init__(self, db):
        self.db = db

    async def create_project(self, project_data: ProjectCreate, current_user):
        collection = await self.db.get_collection("project")
        new_project = {
            "title": project_data.title,
            "description": project_data.description,
            "owner": current_user,
            "members": []
        }

        result = await collection.insert_one(new_project)

        return new_project

    async def get_project_by_id(self, id):
        collection = await self.db.get_collection("project")
        result = await collection.find_one({"_id": ObjectId(id)})
        if not result:
            raise HTTPException(status_code=400, detail="Project does not exist.")
        return serialize_document(result)

    async def get_project_visible_by_user(self, current_user):
        collection = await self.db.get_collection("project")
        result = await collection.find({
            "$or": [
                {"owner": current_user},
                {"members.user_id": current_user}
            ]
        }).to_list()
        if not result:
            raise HTTPException(status_code=400, detail="No projects to display.")
        return serialize_list(result)
    
    async def update_project_by_id(self, project_id, project_data, current_user):
        collection = await self.db.get_collection("project")
        project = await collection.find_one({"_id": ObjectId(project_id)})
        if not project:
            raise HTTPException(status_code=400, detail="Project does not exist.")
        
        project = await check_permission(str(project.get("_id")), ["admin", "editor"], current_user)

        update_data = project_data.model_dump(exclude_none=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields to update.")

        result = await collection.update_one(
            {"_id": ObjectId(project_id)},
            {"$set": update_data}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes were made.")

        updated_project = await collection.find_one({"_id": ObjectId(project_id)})
        return updated_project

    async def add_member_to_project(self, project_id, member, notification_service, current_user, background_tasks):
        collection = await self.db.get_collection("project")
        members = member.model_dump()
        project = await check_permission(project_id, ["admin"], current_user)
        if not project:
            raise HTTPException(status_code=400, detail="Project does not exist.")
        
        new_members = {member["user_id"] for member in members.get("users_id", [])}
        old_members = {member["user_id"] for member in project.get("members", [])}

        duplicates = old_members & new_members
        if duplicates:
            raise HTTPException(status_code=400, detail="User is already a member")
        
        await collection.update_one({"_id": ObjectId(project_id)}, {"$push": {"members": {"$each": members.get("users_id", {})}}})

        message = {
            "type": "project-invite",
            "message": f"Você foi adicionado no projeto: {project.get('title')}",
            "project_id": project_id
        }

        for user_id in members.get("users_id", []):	
            background_tasks.add_task(notification_service.create_notification, user_id.get("user_id"), f"Você foi adicionado no projeto: {project.get('title')}", message.get('type'))

        background_tasks.add_task(send_notification, message, members.get('users_id', []))

        return {"message": "User added to project"}
    
    async def delete_project(self, project_id, current_user):
        collection = await collection.get_collection("project")
        project = await check_permission(project_id, ["admin"], current_user)
        if not project:
            raise HTTPException(status_code=400, detail="Project does not exist.")
        
        await collection.delete_one({"_id": ObjectId(project_id)})
        return True
