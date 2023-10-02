from fastapi import status, HTTPException, APIRouter, BackgroundTasks, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.models.recipes.recipe import Recipe
from uuid import uuid1
import asyncio
from app.background import audit_log_recipes
fake_db = {}

router = APIRouter()


def create_recipe(recipe: Recipe):
    recipe = {"title": recipe.title, "description": recipe.description, "preparation_time": recipe.preparation_time, "ingredients": recipe.ingredients}
    
    return recipe

@router.get("/")
def read_root():
    return JSONResponse(status_code=status.HTTP_200_OK, content=fake_db)

@router.get("/{recipe_id}/")
def get_recipe(recipe_id: str):
    if (recipe_id not in fake_db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    else:
        return JSONResponse(status_code=status.HTTP_200_OK, content=fake_db[recipe_id])


@router.delete("/{recipe_id}/", status_code=204)
def delete_recipe(recipe_id: str):
    if (recipe_id not in fake_db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    else:
        del fake_db[recipe_id]
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "recipe removed"})


@router.patch("/{recipe_id}/", status_code=status.HTTP_201_CREATED)
def patch_recipe(recipe_id: str, recipe: Recipe, bg_task: BackgroundTasks):
    try:
        new_recipe = jsonable_encoder(recipe)
        fake_db[recipe_id] = new_recipe
        bg_task.add_task(audit_log_recipes, recipe_id=str(recipe_id), message="updated")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "recipe updated"})
    except:
        return JSONResponse(content={"message": "invalid operation"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/recipe/", status_code=status.HTTP_201_CREATED)
def post_recipe(recipe: Recipe = Depends(create_recipe)):
    
    recipe_dict = jsonable_encoder(recipe)
    recipe_id = str(uuid1())
    recipe_dict["id"] = recipe_id
    fake_db[recipe_id] = recipe_dict

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=fake_db[recipe_id])


@router.get("/welcome", status_code=status.HTTP_200_OK)
async def welcome():
    await asyncio.sleep(5)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "seja bem-vindo ao fastapi!"})
