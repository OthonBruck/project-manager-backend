from pydantic.generics import GenericModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T") 

class ApiResponse(GenericModel, Generic[T]):
    message: str
    data: Optional[T] = None
