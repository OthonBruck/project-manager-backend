from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, GetCoreSchemaHandler
from pydantic_core import core_schema

class PyObjectId(str):
    """Custom field para suportar ObjectId no Pydantic v2"""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.str_schema()

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponseGet(BaseModel):
    id: PyObjectId
    name: str
    email: EmailStr

class UserResponseCreate(BaseModel):
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
class UserResponseLogin(BaseModel):
    token: str