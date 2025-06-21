from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy import select
from server.configuration.database import DepDatabaseSession
from server.model.to_do_model import ToDoItems



class _ToDoRepository:
    def __init__(self, db: DepDatabaseSession):
        self.db = db
        
    async def get_data(self):
        result = await self.db.execute(select(ToDoItems))
        return result.scalars().all()
    
    async def add_to_do_item(self, item: ToDoItems):
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item
        
    
    async def get_todo(self, todo_id: int):
        todo = await self.db.execute(select(ToDoItems).filter(ToDoItems.id == todo_id))
        todo_item = todo.scalar_one_or_none()
        if not todo_item:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
        return todo_item
    
    async def get_item_by_id(self, item_id: int):
        result = await self.db.execute(select(ToDoItems).filter(ToDoItems.id == item_id))
        return result.scalar_one_or_none()

    async def delete_to_do_item(self, item: ToDoItems):
        await self.db.delete(item)
        await self.db.commit()


ToDoRepository = Annotated[_ToDoRepository, Depends(_ToDoRepository)]