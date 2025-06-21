from datetime import datetime
from sqlalchemy import Integer, String, func, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from server.model.meta import BaseEntity




class ToDoItems(BaseEntity):
    __tablename__ = "todo_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    completed: Mapped[Optional[bool]] = mapped_column(
        Boolean, server_default="false", nullable=True
    )
