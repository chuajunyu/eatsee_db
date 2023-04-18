
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
    age: int
    gender: int

class Telename(BaseModel):
    telename: str

# class UserID(BaseModel):
#     userid: int

class Preferences(BaseModel):
    preferences: list[int]


@app.post("/create_user/")
async def create_user(user: User):
    return mc.insert_user(user.availability, user.telename)

@app.post("/change_age_preferecnces/")
async def change_age_preferecnces(telename: Telename, preferences: Preferences):
    return mc.change_age_pref(telename.telename, preferences.preferences, "age_ref", "age_ref_id")

@app.post("/change_cuisine_preferecnces/")
async def change_cuisine_preferecnces(telename: Telename, preferences: Preferences):
    return mc.change_cuisine_pref(telename.telename, preferences.preferences, "cuisine_ref", "cuisine_ref_id")

@app.post("/change_diet_preferecnces/")
async def change_diet_preferecnces(telename: Telename, preferences: Preferences):
    return mc.change_diet_preferecnces(telename.telename, preferences.preferences, "diet_ref", "diet_ref_id")