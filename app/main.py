from typing import Union
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import random


fake_db = {}


class Recipes(BaseModel):
    title: str
    description: str
    preparation_time: str
    Ingredients: list[str]


app = FastAPI()


@app.get("/")
def read_root():
    return fake_db


def generate_id():
    return random.randint(1, 100000)


@app.get("/recipes/{recipe_id}/")
def get_recipe(recipe_id: int):
    if (recipe_id in fake_db):
        return fake_db[recipe_id]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")


@app.delete("/recipes/{recipe_id}/", status_code=204)
def delete_recipe(recipe_id: int):
    if (recipe_id in fake_db):
        del fake_db[recipe_id]
        return 'Deletado'
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")


@app.patch("/recipes/{recipe_id}/", status_code=status.HTTP_201_CREATED)
def patch_recipe(recipe_id: int, recipe: Recipes):
    if (recipe_id in fake_db):
        new_recipe = jsonable_encoder(recipe)
        fake_db[recipe_id] = new_recipe
        return new_recipe
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")


@app.post("/recipes/", status_code=status.HTTP_201_CREATED)
def create_recipe(recipe: Recipes):
    recipe_id = generate_id()
    json_compatible_item_data = jsonable_encoder(recipe)
    json_compatible_item_data["id"] = recipe_id
    fake_db[recipe_id] = json_compatible_item_data

    return json_compatible_item_data
