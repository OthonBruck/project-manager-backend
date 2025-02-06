from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import core_schema

class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.str_schema()

class ProjectCreate(BaseModel):
    title: str
    description: str

class ProjectResponseGet(BaseModel):
    id: PyObjectId
    title: str
    description: str

class ProjectResponseCreate(BaseModel):
    title: str

class ProjectAddMember(BaseModel):
    user_id: PyObjectId