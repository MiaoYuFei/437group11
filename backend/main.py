from uuid import uuid4
from entity.user import *
from firebase import *
from flask import Flask, jsonify, make_response, request, session
from flask_session import Session

app = Flask("stocknews")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

fb = firebase()
db = fb.get_db()

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
        session["userId"] = user.id
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
        "code": 500,
        "data": {}
    }
    if ("userId" in session and session["userId"] != None):
        user = get_user_by_id(db, session["userId"])
        result["code"] = 200
        result["data"]["id"] = user.id
        result["data"]["username"] = user.username
    else:
        result["code"] = 403
    return make_response(jsonify(result), 200)

@app.route('/api/user/signout', methods=['POST'])
def signout():
    result = { 
        "code": 200
    }
    session["userId"] = None
    return make_response(jsonify(result), 200)

if __name__ == "__main__":
    app.run(host="::", port=8080)
