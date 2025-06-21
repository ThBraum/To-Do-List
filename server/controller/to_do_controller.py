from typing import List, Optional
from fastapi import APIRouter

from server.schema.to_do_schema import ToDoInput, ToDoOutput
from server.service.to_do_service import ToDoService


router = APIRouter(tags=["To-Do"])


@router.get("/get-to-do-list", summary="Get To-Do List", response_model=List[ToDoOutput])
async def get_to_do_list(service: ToDoService):
    """
    Retrieve the list of to-do items.
    """
    return await service.get_to_do_list()


@router.post("/add-to-do", summary="Add To-Do Item", response_model=ToDoOutput)
async def add_to_do_item(data: ToDoInput, service: ToDoService):
    """
    Add a new to-do item.
    """
    return await service.add_to_do_item(data=data)


@router.delete("/delete-to-do-item/{item_id}", summary="Delete a To-Do Item")
async def delete_to_do_item(item_id: int, service: ToDoService):
    """
    Delete the To-Do item by ID.
    """
    return await service.delete_to_do_item(item_id)

@router.get("/to_to/{item_id}", summary="Get To-Do Item", response_model=ToDoOutput)
async def get_to_do_item(item_id: int, service: ToDoService):
    """
    Retrieve a specific to-do item by its ID.
    """
    return await service.get_to_do_item(item_id=item_id)