from typing import Annotated, List, Optional

from fastapi import Depends, HTTPException
from server.configuration.database import DepDatabaseSession
from server.model.to_do_model import ToDoItems
from server.repository.to_do_repository import _ToDoRepository, ToDoRepository
from server.schema.to_do_schema import NewToDoItem, ToDoInput, ToDoOutput
from sqlalchemy import func, text
from datetime import datetime


class _ToDoService:
    def __init__(self, db: DepDatabaseSession):
        self.db = db
        self.repository: _ToDoRepository = ToDoRepository(db)
        
    async def get_to_do_list(self) -> Optional[List[ToDoOutput]]:
        data = await self.repository.get_data()
        
        if data:
            return [ToDoOutput.model_validate(todo) for todo in data]
        
        return []
    
    
    async def add_to_do_item(self, data: ToDoInput):
        new_to_do_item = ToDoItems(
            title=data.title,
            description=data.description if data.description else None,
            completed=data.completed if data.completed else False,
            created_at=datetime.now(),
        )

        new_item = await self.repository.add_to_do_item(new_to_do_item)
        new_item.created_at = new_item.created_at.isoformat()
        return ToDoOutput.model_validate(new_item)
    
    
    async def delete_to_do_item(self, item_id: int):
        item = await self.repository.get_item_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="To-Do item not found")

        await self.repository.delete_to_do_item(item)
        return {"message": "Item deleted successfully"}
    
    
    async def get_to_do_item(self, item_id: int) -> Optional[ToDoOutput]:
        query = text("""
        SELECT id, title, description, completed, created_at, updated_at
        FROM todo_items
        WHERE id = :item_id
        """)
        result = await self.db.execute(query, {"item_id": item_id})
        item = result.fetchone()
        if not item:
            raise HTTPException(status_code=404, detail="To-Do item not found")
        return ToDoOutput.model_validate(item)
    
        
ToDoService = Annotated[_ToDoService, Depends(_ToDoService)]