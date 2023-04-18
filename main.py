
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


@app.post("/create_user/")
async def create_user(user: User):
    return mc.insert_user(user.availability, user.telename, user.age, user.gender)


# Go make this into a single class  so its nicer
class Telename(BaseModel):
    telename: str

class Preferences(BaseModel):
    preferences: list[int]


@app.post("/change_age_preferences/")
async def change_age_preferences(telename: Telename, preferences: Preferences):
    return mc.change_age_pref(telename.telename, preferences.preferences, "age_ref", "age_ref_id")

@app.post("/change_cuisine_preferences/")
async def change_cuisine_preferences(telename: Telename, preferences: Preferences):
    return mc.change_cuisine_pref(telename.telename, preferences.preferences, "cuisine_ref", "cuisine_ref_id")

@app.post("/change_diet_preferences/")
async def change_diet_preferences(telename: Telename, preferences: Preferences):
    return mc.change_diet_pref(telename.telename, preferences.preferences, "diet_ref", "diet_ref_id")

@app.post("/change_gender_preferences/")
async def change_diet_preferences(telename: Telename, preferences: Preferences):
    return mc.change_diet_pref(telename.telename, preferences.preferences, "gender_ref", "gender_ref_id")