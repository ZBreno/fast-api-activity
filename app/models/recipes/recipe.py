from uuid import uuid1
from pydantic import BaseModel
from typing import List

class Recipe(BaseModel):
    title: str
    description: str
    preparation_time: str
    ingredients: List[str]
    
# class Recipe:
#     def __init__(self, title: str, description: str, preparation_time: str, ingredients: List[str]):
#         self.id = str(uuid1())
#         self.title = title
#         self.description = description
#         self.preparation_time = preparation_time
#         self.ingredients = ingredients