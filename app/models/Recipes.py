from pydantic import BaseModel

class Recipe(BaseModel):
    title: str
    description: str
    preparation_time: str
    Ingredients: list[str]