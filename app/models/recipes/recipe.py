from pydantic import BaseModel
from uuid import UUID

class Recipe(BaseModel):
    id: UUID
    title: str
    description: str
    preparation_time: str
    Ingredients: list[str]