
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

@app.post("/select_age_preferences/")
async def select_age_preferences(telename: Telename):
    return mc.select_pref(telename.telename, "age_ref_id", "age_ref")

@app.post("/select_gender_preferences/")
async def select_gender_preferences(telename: Telename):
    return mc.select_pref(telename.telename, "gender_ref_id", "gender_ref")

@app.post("/select_cuisine_preferences/")
async def select_cuisine_preferences(telename: Telename):
    return mc.select_pref(telename.telename, "cuisine_ref_id", "cuisine_ref")

@app.post("/select_diet_preferences/")
async def select_diet_preferences(telename: Telename):
    return mc.select_pref(telename.telename, "diet_ref_id", "diet_ref")

@app.post("/delete_user/")
async def delete_user(telename: Telename):
    return mc.delete_user(telename.telename)


class UserCharacteristics(BaseModel):
    telename: str
    characteristic: int

@app.post("/change_age/")
async def change_age(usercharacteristic: UserCharacteristics):
    return mc.change_user_info(usercharacteristic.telename, usercharacteristic.characteristic, "age_ref_id", "age")

@app.post("/change_gender/")
async def change_gender(usercharacteristic: UserCharacteristics):
    return mc.change_user_info(usercharacteristic.telename, usercharacteristic.characteristic, "gender_ref_id", "gender")


class UserAvailability(BaseModel):
    telename: str
    availability: bool

@app.post("/change_availability/")
async def change_availability(useravailability: UserAvailability):
    return mc.change_user_info(useravailability.telename, useravailability.availability, "availability", "availability")


class Preferences(BaseModel):
    telename:str
    preferences: list[int]

@app.post("/change_age_preferences/")
async def change_age_preferences(preferences: Preferences):
    return mc.change_pref(preferences.telename, preferences.preferences, "age_ref_id", "age_ref", True, True)

@app.post("/change_gender_preferences/")
async def change_gender_preferences(preferences: Preferences):
    return mc.change_pref(preferences.telename, preferences.preferences, "gender_ref_id", "gender_ref", True, True)

@app.post("/change_cuisine_preferences/")
async def change_cuisine_preferences(preferences: Preferences):
    return mc.change_pref(preferences.telename, preferences.preferences, "cuisine_ref_id", "cuisine_ref", True, True)

@app.post("/change_diet_preferences/")
async def change_diet_preferences(preferences: Preferences):
    return mc.change_pref(preferences.telename, preferences.preferences, "diet_ref_id", "diet_ref", True, True)

@app.post("/add_age_preferences/")
async def add_age_preferences(preferences: Preferences):
    return mc.change_pref(preferences.telename, preferences.preferences, "age_ref_id", "age_ref", True, False)

@app.post("/add_gender_preferences/")
async def add_gender_preferences(preferences: Preferences):
    return mc.change_pref(preferences.telename, preferences.preferences, "gender_ref_id", "gender_ref", True, False)

@app.post("/add_cuisine_preferences/")
async def add_cuisine_preferences(preferences: Preferences):
    return mc.change_pref(preferences.telename, preferences.preferences, "cuisine_ref_id", "cuisine_ref", True, False)

@app.post("/add_diet_preferences/")
async def add_diet_preferences(preferences: Preferences):
    return mc.change_pref(preferences.telename, preferences.preferences, "diet_ref_id", "diet_ref", True, False)

@app.post("/delete_age_preferences/")
async def delete_age_preferences(preferences: Preferences):
    return mc.change_pref(preferences.telename, preferences.preferences, "age_ref_id", "age_ref", False, True)

@app.post("/delete_gender_preferences/")
async def delete_gender_preferences(preferences: Preferences):
    return mc.change_pref(preferences.telename, preferences.preferences, "gender_ref_id", "gender_ref", False, True)

@app.post("/delete_cuisine_preferences/")
async def delete_cuisine_preferences(preferences: Preferences):
    return mc.change_pref(preferences.telename, preferences.preferences, "cuisine_ref_id", "cuisine_ref", False, True)

@app.post("/delete_diet_preferences/")
async def delete_diet_preferences(preferences: Preferences):
    return mc.change_pref(preferences.telename, preferences.preferences, "diet_ref_id", "diet_ref", False, True)


# No classes

@app.post("/show_age_choices/")
async def show_one_choice():
    return mc.show_one_choice("age_id", "age_range", "age")

@app.post("/show_gender_choices/")
async def show_one_choice():
    return mc.show_one_choice("gender_id", "gender", "gender")

@app.post("/show_cuisine_choices/")
async def show_one_choice():
    return mc.show_one_choice("cuisine_id", "cuisine", "cuisine")

@app.post("/show_diet_choices/")
async def show_one_choice():
    return mc.show_one_choice("diet_id", "diet_res_type", "diet")

@app.post("/show_all_choices/")
async def show_all_choices():
    return mc.show_all_choices()

