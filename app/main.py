from fastapi import FastAPI, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.models.Recipes import Recipe
import random


fake_db = {}


app = FastAPI()


@app.get("/")
def read_root():
    return JSONResponse(status_code=status.HTTP_200_OK, content=fake_db )


def generate_id():
    return random.randint(1, 100000)


@app.get("/recipes/{recipe_id}/")
def get_recipe(recipe_id: int):
    if (recipe_id not in fake_db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    else:
        return JSONResponse(status_code=status.HTTP_200_OK, content=fake_db[recipe_id] )


@app.delete("/recipes/{recipe_id}/", status_code=204)
def delete_recipe(recipe_id: int):
    if (recipe_id not in fake_db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    else:
        del fake_db[recipe_id]
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "recipe removed"})


@app.patch("/recipes/{recipe_id}/", status_code=status.HTTP_201_CREATED)
def patch_recipe(recipe_id: int, recipe: Recipe):
    if recipe_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    else:
        new_recipe = jsonable_encoder(recipe)
        fake_db[recipe_id] = new_recipe
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "recipe updated"})


@app.post("/recipes/", status_code=status.HTTP_201_CREATED)
def create_recipe(recipe: Recipe):

    recipe_id = generate_id()
    json_compatible_item_data = jsonable_encoder(recipe)
    json_compatible_item_data["id"] = recipe_id
    fake_db[recipe_id] = json_compatible_item_data

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=fake_db[recipe_id])

