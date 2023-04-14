
from Classes import MainController
from Classes import ConfigManager

from fastapi import FastAPI
from pydantic import BaseModel


ConfigManager(r"dev.config")
app = FastAPI()
mc = MainController()

@app.get("/")
async def root():
    return {"message": "Hello World"}


class User(BaseModel):
    availability: bool
    telename: str


@app.post("/create_user/")
async def create_user(user: User):
    return mc.insert_user(user.availability, user.telename)
    