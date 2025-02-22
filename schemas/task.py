from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import core_schema
from typing import Optional

class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.str_schema()

class TaskCreate(BaseModel):
    project_id: str
    title: str
    description: str

class TaskResponseGet(BaseModel):
    id: PyObjectId
    title: str
    description: str

class TaskResponseCreate(BaseModel):
    title: str
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None