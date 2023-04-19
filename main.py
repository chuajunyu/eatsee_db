
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


class Telename(BaseModel):
    telename: str

@app.post("/show_profile/")
async def show_profile(telename: Telename):
    return mc.show_profile(telename.telename)

@app.post("/get_user_id/")
async def get_user_id(telename: Telename):
    return mc.get_user_id(telename.telename)

@app.post("/queue/")
async def queue(telename: Telename):
    return mc.queue(telename.telename)

@app.post("/dequeue/")
async def deueue(telename: Telename):
    return mc.dequeue(telename.telename)

@app.post("/match/")
async def match(telename: Telename):
    return mc.person_match(telename.telename)


class Preferences(BaseModel):
    telename:str
    preferences: list[int]


@app.post("/change_age_preferences/")
async def change_age_preferences(preferences: Preferences):
    return mc.change_pref(preferences.telename, preferences.preferences, "age_ref", "age_ref_id")

@app.post("/change_gender_preferences/")
async def change_diet_preferences(preferences: Preferences):
    return mc.change_pref(preferences.telename, preferences.preferences, "gender_ref", "gender_ref_id")

@app.post("/change_cuisine_preferences/")
async def change_cuisine_preferences(preferences: Preferences):
    return mc.change_pref(preferences.telename, preferences.preferences, "cuisine_ref", "cuisine_ref_id")

@app.post("/change_diet_preferences/")
async def change_diet_preferences(preferences: Preferences):
    return mc.change_pref(preferences.telename, preferences.preferences, "diet_ref", "diet_ref_id")



@app.post("/show_age_choices/")
async def show_choices():
    return mc.show_choices("age_range", "age")

@app.post("/show_gender_choices/")
async def show_choices():
    return mc.show_choices("gender", "gender")

@app.post("/show_cuisine_choices/")
async def show_choices():
    return mc.show_choices("cuisine", "cuisine")

@app.post("/show_diet_choices/")
async def show_choices():
    return mc.show_choices("diet_res_type", "diet")

@app.post("/show_all_choices/")
async def show_choices():
    return mc.show_all_choices()

