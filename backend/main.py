from uuid import uuid4
from entity.user import *
from firebase import *
from flask import Flask, jsonify, make_response, request

app = Flask("stocknews")
fb = firebase()
db = fb.get_db()

@app.route("/")
def home():
    return "Hello, World!"

@app.route('/api/user/signin', methods=['POST'])
def signin():
    username = request.form["username"]
    password = request.form["password"]
    result = {
        "code": 500,
        "data": {}
    }
    user = get_user_by_username(db, username)
    if user == None:
        result["code"] = 403
        result["data"]["reason"] = "User doesn't exist."
        return make_response(jsonify(result), 200)
    if authenticate_user(db, user.id, password):
        result["code"] = 200
        return make_response(jsonify(result), 200)
    else:
        result["code"] = 403
        result["data"]["reason"] = "Wrong credentials."
        return make_response(jsonify(result), 200)

@app.route('/api/user/register', methods=['POST'])
def register():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    result = {
        "code": 500,
        "data": {}
    }
    user = get_user_by_username(db, username)
    if user != None:
        result["code"] = 403
        result["data"]["reason"] = "Duplicate username."
        return make_response(jsonify(result), 200)
    user = User.from_dict({
        "id": str(uuid4()),
        "username": username,
        "email": email,
        "password": password
    })
    add_user(db, user)
    result["code"] = 200
    return make_response(jsonify(result), 200)

@app.route('/api/user/status', methods=['POST'])
def status():
    result = { 
        "code": 200,
        "username": "username"
    }
    return make_response(jsonify(result), 200)

@app.route('/api/user/signout', methods=['POST'])
def signout():
    result = { 
        "code": 200
    }
    return make_response(jsonify(result), 200)

if __name__ == "__main__":
    app.run(port=9000)
