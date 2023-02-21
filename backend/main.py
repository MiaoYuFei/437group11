from uuid import uuid4
from entity.user import *
from firebase import *
from flask import Flask

app = Flask("stocknews")
fb = firebase()
db = fb.get_db()

@app.route("/")
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run()
    user = User.from_dict({
        "id": str(uuid4()),
        "username": "test5",
        "email": "test5@gmail.com",
        "password": "test5"
    })
    add_user(db, user)
    user = get_user_by_id(db, "86f80f93-d251-4302-a711-6713a002bf79")
    print(user)
    user.email="test@pmail.com"
    update_user(db, user)
    user = get_user_by_id(db, "86f80f93-d251-4302-a711-6713a002bf79")
    print(user)
    print(authenticate_user(db, "86f80f93-d251-4302-a711-6713a002bf79", "test2"))
