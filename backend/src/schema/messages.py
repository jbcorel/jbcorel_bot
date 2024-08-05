from fastapi import status
from pydantic import BaseModel, Field
from typing import Annotated, List
from datetime import datetime


class Message(BaseModel):
    author: str
    content: Annotated[str, Field(min_length=1)]
    date_created: datetime
    
class Response(BaseModel):
    data: List[Message]
    status: int = Field(default=status.HTTP_200_OK)
    message: str = Field(default='Successful operation')
    