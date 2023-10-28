from fastapi import FastAPI
from api import admin, login, attendance, members, trainers


app = FastAPI()
app.include_router(admin.router)
app.include_router(login.router)
app.include_router(attendance.router)
app.include_router(members.router)
app.include_router(trainers.router)
