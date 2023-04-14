from .QueryManager import QueryManager

class MainController:
    def __init__(self):
        self.qm = QueryManager()

    def select_user(self, telename):
        return self.qm.select_user(telename)

    def insert_user(self, availability, telename):
        if self.qm.select_user(telename):  # Check if user alr exists
            return {"message": "User Creation Failed: User already Exists"}
        self.qm.insert_user(availability, telename)
        return {"message": "User Successfully Created"}
