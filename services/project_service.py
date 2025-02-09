from schemas.project import ProjectCreate
from fastapi import HTTPException
from bson.objectid import ObjectId
from utils.functions import serialize_document, check_permission
from services.websocket_service import send_notification

class ProjectService:
    def __init__(self, db):
        self.db = db.get_collection("project")
    
    async def create_project(self, project_data: ProjectCreate, current_user):
        new_project = {
            "title": project_data.title,
            "description": project_data.description,
            "owner": current_user,
            "members": []
        }
        await self.db.insert_one(new_project)

        return new_project

    async def get_project_by_id(self, id):
        result = await self.db.find_one({"_id": ObjectId(id)})
        if not result:
            raise HTTPException(status_code=400, detail="Project does not exist.")
        return serialize_document(result)

    async def add_member_to_project(self, project_id, member, notification_service, current_user, background_tasks):
        members = member.model_dump()
        project = await check_permission(project_id, ["admin"], current_user, db=self.db)
        if not project:
            raise HTTPException(status_code=400, detail="Project does not exist.")
        
        new_members = {member["user_id"] for member in members.get("users_id", [])}
        old_members = {member["user_id"] for member in project.get("members", [])}

        duplicates = old_members & new_members
        if duplicates:
            raise HTTPException(status_code=400, detail="User is already a member")
        
        await self.db.update_one({"_id": ObjectId(project_id)}, {"$push": {"members": {"$each": members.get("users_id", {})}}})

        message = {
            "type": "project-invite",
            "message": f"Você foi adicionado no projeto: {project.get('title')}",
            "project_id": project_id
        }
        #TODO: after changing the way it insert the new members, we need to change how is sent the notifications
        for user_id in members.get("users_id", []):	
            background_tasks.add_task(notification_service.create_notification, user_id.get("user_id"), f"Você foi adicionado no projeto: {project.get('title')}", message.get('type'))

        background_tasks.add_task(send_notification, message, members.get('users_id', []))

        return {"message": "User added to project"}
