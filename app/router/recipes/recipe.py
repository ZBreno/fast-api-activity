from fastapi import status, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.models.recipes.recipe import Recipe
from uuid import uuid1
import asyncio

fake_db = {}

router = APIRouter()


@router.get("/")
def read_root():
    return JSONResponse(status_code=status.HTTP_200_OK, content=fake_db)


@router.get("/{recipe_id}/")
def get_recipe(recipe_id: int):
    if (recipe_id not in fake_db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    else:
        return JSONResponse(status_code=status.HTTP_200_OK, content=fake_db[recipe_id])


@router.delete("/{recipe_id}/", status_code=204)
def delete_recipe(recipe_id: int):
    if (recipe_id not in fake_db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    else:
        del fake_db[recipe_id]
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "recipe removed"})


@router.patch("/{recipe_id}/", status_code=status.HTTP_201_CREATED)
def patch_recipe(recipe_id: int, recipe: Recipe):
    if recipe_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    else:
        new_recipe = jsonable_encoder(recipe)
        fake_db[recipe_id] = new_recipe
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "recipe updated"})


@router.post("/recipe/", status_code=status.HTTP_201_CREATED)
def create_recipe(recipe: Recipe):

    recipe_id = str(uuid1())
    json_compatible_item_data = {
        "id": str(uuid1()),
        "title": recipe.title,
        "description": recipe.description,
        "preparation_time": recipe.preparation_time,
        "Ingredients": recipe.Ingredients
    }
    fake_db[recipe_id] = json_compatible_item_data

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=fake_db[recipe_id])


@router.post("/saberne", status_code=status.HTTP_200_OK)
async def welcome():
    await asyncio.sleep(5)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "oi, tudo bem?"})
