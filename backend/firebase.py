import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class firebase:
    cred = credentials.Certificate("stocknews-aa6b7-1e99a4c22877.json")
    app = None
    db = None

    def __init__(self):
        self.app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

    def get_app(self):
        return self.app

    def get_db(self):
        return self.db
