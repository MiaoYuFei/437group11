from uuid import uuid4
from entity.user import *
from firebase import *
from flask import Flask
from flask import request

app = Flask("stocknews")
fb = firebase()
db = fb.get_db()

@app.route("/")
def home():
    return "Hello, World!"

@app.route('/api/login', methods=['POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = get_user_by_username(db, username)
    if user == None:
        return "User doesn't exist!"
    result = authenticate_user(db, user.id, password)
    if result:
        return "Congratulations! Login successful!"
    else:
        return "Wrong password!!"

@app.route('/api/register', methods=['POST'])
def register():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    user = get_user_by_username(db, username)
    if user != None:
        return "Duplicate username!"
    user = User.from_dict({
        "id": str(uuid4()),
        "username": username,
        "email": email,
        "password": password
    })
    add_user(db, user)
    return "User registration successful!"

if __name__ == "__main__":
    app.run(port=9001)
