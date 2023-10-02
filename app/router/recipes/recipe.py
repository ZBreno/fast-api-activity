from fastapi import status, HTTPException, APIRouter, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.models.recipes.recipe import Recipe
from uuid import uuid1
import asyncio
from datetime import datetime

fake_db = {}

router = APIRouter()


@router.get("/")
def read_root():
    return JSONResponse(status_code=status.HTTP_200_OK, content=fake_db)

def audit_log_recipes(recipe_id: str, message=""):
    with open("C:/Users/breno/OneDrive/Documentos/Pyhton/Desenvolvimento de Sistemas Corporativos/Atividade de Fast-API 01/app/audit_log.txt", mode="a") as logfile:
        content = f"\nrecipe {recipe_id} executed {message} at {datetime.now()}"
        logfile.write(content)


@router.get("/{recipe_id}/")
def get_recipe(recipe_id: int):
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


@router.get("/welcome", status_code=status.HTTP_200_OK)
async def welcome():
    await asyncio.sleep(5)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "seja bem-vindo ao fastapi!"})
