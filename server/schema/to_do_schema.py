from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ToDoOutput(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
        
class ToDoInput(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
    
    class Config:
        from_attributes = True
        
        
class NewToDoItem(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
        
        