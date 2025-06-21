from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text

from server.configuration.database import DepDatabaseSession

router = APIRouter(tags=["Server"])


@router.get("/ping/")
async def ping():
    return "pong"