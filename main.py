
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
    user_id: int
    telename: str
    age: int
    gender: int

@app.post("/create_user/")
async def create_user(user: User):
    return mc.insert_user(user.user_id, user.telename, user.age, user.gender)


class Telename(BaseModel):
    telename: str

@app.post("/get_user_id/")
async def get_user_id(telename: Telename):
    return mc.get_user_id(telename.telename)


class UserId(BaseModel):
    user_id: int

@app.post("/show_profile/")
async def show_profile(user_id: UserId):
    return mc.show_profile(user_id.user_id)

@app.post("/queue/")
async def queue(user_id: UserId):
    return mc.queue(user_id.user_id)

@app.post("/dequeue/")
async def dequeue(user_id: UserId):
    return mc.dequeue(user_id.user_id)

@app.post("/match/")
async def match(user_id: UserId):
    return mc.person_match(user_id.user_id)

@app.post("/select_age_preferences/")
async def select_age_preferences(user_id: UserId):
    return mc.select_pref(user_id.user_id, "age_ref_id", "age_ref")

@app.post("/select_gender_preferences/")
async def select_gender_preferences(user_id: UserId):
    return mc.select_pref(user_id.user_id, "gender_ref_id", "gender_ref")

@app.post("/select_cuisine_preferences/")
async def select_cuisine_preferences(user_id: UserId):
    return mc.select_pref(user_id.user_id, "cuisine_ref_id", "cuisine_ref")

@app.post("/select_diet_preferences/")
async def select_diet_preferences(user_id: UserId):
    return mc.select_pref(user_id.user_id, "diet_ref_id", "diet_ref")

@app.post("/select_pax_preferences/")
async def select_pax_preferences(user_id: UserId):
    return mc.select_pref(user_id.user_id, "pax_ref_id", "pax_ref")

@app.post("/check_users_for_user/")
async def check_users_for_user(user_id: UserId):
    return mc.check_table_for_user(user_id.user_id, "users")

@app.post("/check_queue_for_user/")
async def check_queue_for_user(user_id: UserId):
    return mc.check_table_for_user(user_id.user_id, "queue")

@app.post("/check_chat_for_user/")
async def check_chat_for_user(user_id: UserId):
    return mc.check_table_for_user(user_id.user_id, "chat")

@app.post("/delete_user/")
async def delete_user(user_id: UserId):
    return mc.delete_user(user_id.user_id)


class UserCharacteristics(BaseModel):
    user_id: int
    characteristic: int

@app.post("/change_age/")
async def change_age(usercharacteristic: UserCharacteristics):
    return mc.change_user_info(usercharacteristic.user_id, usercharacteristic.characteristic, "age_ref_id", "age")

@app.post("/change_gender/")
async def change_gender(usercharacteristic: UserCharacteristics):
    return mc.change_user_info(usercharacteristic.user_id, usercharacteristic.characteristic, "gender_ref_id", "gender")


class UserAvailability(BaseModel):
    user_id: int
    availability: bool

@app.post("/change_availability/")
async def change_availability(useravailability: UserAvailability):
    return mc.change_user_info(useravailability.user_id, useravailability.availability, "availability", "availability")


class Preferences(BaseModel):
    user_id: int
    preferences: list[int]

@app.post("/change_age_preferences/")
async def change_age_preferences(preferences: Preferences):
    return mc.change_pref(preferences.user_id, preferences.preferences, "age_ref_id", "age_ref", True, True)

@app.post("/change_gender_preferences/")
async def change_gender_preferences(preferences: Preferences):
    return mc.change_pref(preferences.user_id, preferences.preferences, "gender_ref_id", "gender_ref", True, True)

@app.post("/change_cuisine_preferences/")
async def change_cuisine_preferences(preferences: Preferences):
    return mc.change_pref(preferences.user_id, preferences.preferences, "cuisine_ref_id", "cuisine_ref", True, True)

@app.post("/change_diet_preferences/")
async def change_diet_preferences(preferences: Preferences):
    return mc.change_pref(preferences.user_id, preferences.preferences, "diet_ref_id", "diet_ref", True, True)

@app.post("/change_pax_preferences/")
async def change_pax_preferences(preferences: Preferences):
    return mc.change_pref(preferences.user_id, preferences.preferences, "pax_ref_id", "pax_ref", True, True)

@app.post("/add_age_preferences/")
async def add_age_preferences(preferences: Preferences):
    return mc.change_pref(preferences.user_id, preferences.preferences, "age_ref_id", "age_ref", True, False)

@app.post("/add_gender_preferences/")
async def add_gender_preferences(preferences: Preferences):
    return mc.change_pref(preferences.user_id, preferences.preferences, "gender_ref_id", "gender_ref", True, False)

@app.post("/add_cuisine_preferences/")
async def add_cuisine_preferences(preferences: Preferences):
    return mc.change_pref(preferences.user_id, preferences.preferences, "cuisine_ref_id", "cuisine_ref", True, False)

@app.post("/add_diet_preferences/")
async def add_diet_preferences(preferences: Preferences):
    return mc.change_pref(preferences.user_id, preferences.preferences, "diet_ref_id", "diet_ref", True, False)

@app.post("/add_pax_preferences/")
async def add_pax_preferences(preferences: Preferences):
    return mc.change_pref(preferences.user_id, preferences.preferences, "diet_pax_id", "pax_ref", True, False)

@app.post("/delete_age_preferences/")
async def delete_age_preferences(preferences: Preferences):
    return mc.change_pref(preferences.user_id, preferences.preferences, "age_ref_id", "age_ref", False, True)

@app.post("/delete_gender_preferences/")
async def delete_gender_preferences(preferences: Preferences):
    return mc.change_pref(preferences.user_id, preferences.preferences, "gender_ref_id", "gender_ref", False, True)

@app.post("/delete_cuisine_preferences/")
async def delete_cuisine_preferences(preferences: Preferences):
    return mc.change_pref(preferences.user_id, preferences.preferences, "cuisine_ref_id", "cuisine_ref", False, True)

@app.post("/delete_diet_preferences/")
async def delete_diet_preferences(preferences: Preferences):
    return mc.change_pref(preferences.user_id, preferences.preferences, "diet_ref_id", "diet_ref", False, True)

@app.post("/delete_pax_preferences/")
async def delete_pax_preferences(preferences: Preferences):
    return mc.change_pref(preferences.user_id, preferences.preferences, "diet_pax_id", "pax_ref", False, True)

# class AddChatroomUsers(BaseModel):
#     chatroom_id: int
#     user_id_list: list[int]

class UserIdList(BaseModel):
    user_id_list: list[int]

@app.post("/delete_user_multiple/")
async def delete_user_multiple(deleteusermultiple: UserIdList):
    return mc.delete_user(deleteusermultiple.user_id_list)

@app.post("/add_chatroom_user/")
async def add_chatroom_user(addchatroomusers: UserIdList):
    return mc.add_chatroom_user(addchatroomusers.user_id_list)

@app.post("/delete_chatroom_user/")
async def delete_chatroom_user(dltchatroomusers: UserIdList):
    return mc.delete_chatroom_user(dltchatroomusers.user_id_list)

class SelectChatroomUsers(BaseModel):
    chatroom_id: int

@app.post("/select_chatroom_user/")
async def select_chatroom_user(selectchatroomusers: SelectChatroomUsers):
    return mc.select_chatroom_user(selectchatroomusers.chatroom_id)

class SelectChatroom(BaseModel):
    user_id: int

@app.post("/select_chatroom/")
async def select_chatroom(selectchatroom: SelectChatroom):
    return mc.select_chatroom(selectchatroom.user_id)


class FindRestaurants(BaseModel):
    user_coords: list
    town: str
    max_distance: float
    cuisine_whitelist: list
    diet_whitelist: list
    cuisine_diet_blacklist: list
    include_all_cuisines: bool

@app.post("/find_restaurants/")
async def find_restaurants(findrestaurants: FindRestaurants):
    return mc.find_restaurants(findrestaurants.user_coords, findrestaurants.town, findrestaurants.max_distance, findrestaurants.cuisine_whitelist, findrestaurants.diet_whitelist, findrestaurants.cuisine_diet_blacklist, findrestaurants.include_all_cuisines)


class FindRestaurantsTgt(BaseModel):
    user_id_list: list[int]
    user_coords: list
    town: str
    max_distance: float

@app.post("/find_restaurants_tgt/")
async def find_restaurants_tgt(findrestaurantstgt: FindRestaurantsTgt):
    return mc.find_restaurants_together(findrestaurantstgt.user_id_list, findrestaurantstgt.user_coords, findrestaurantstgt.town, findrestaurantstgt.max_distance)


# No classes

@app.post("/show_age_choices/")
async def show_age_choice():
    return mc.show_one_choice("age_id", "age_range", "age")

@app.post("/show_gender_choices/")
async def show_gender_choice():
    return mc.show_one_choice("gender_id", "gender", "gender")

@app.post("/show_cuisine_choices/")
async def show_cuisine_choice():
    return mc.show_one_choice("cuisine_id", "cuisine", "cuisine")

@app.post("/show_diet_choices/")
async def show_diet_choice():
    return mc.show_one_choice("diet_id", "diet_res_type", "diet")

@app.post("/show_pax_choices/")
async def show_pax_choice():
    return mc.show_one_choice("pax_id", "pax_number", "pax")

@app.post("/show_all_choices/")
async def show_all_choices():
    return mc.show_all_choices()

@app.post("/test_function/")
async def test_fucntion():
    return mc.test_function()
