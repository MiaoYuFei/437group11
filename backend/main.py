#!/usr/bin/env python3

from flask import Flask, jsonify, make_response, request, session
from flask_session import Session

import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyB8eOEHSXykFluDLDDeBe7wkyR55stIAAM",
  "authDomain": "stocknews-aa6b7.firebaseapp.com",
  "databaseURL": "https://stocknews-aa6b7.firebaseio.com",
  "projectId": "stocknews-aa6b7",
  "storageBucket": "stocknews-aa6b7.appspot.com",
  "messagingSenderId": "425418971970",
  "appId": "1:425418971970:web:565abf186779c1edf306db",
  "measurementId": "G-SYMFM414XJ"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

app = Flask("stocknews")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/api/user/signin", methods=["POST"])
def signin():
    email = request.form["email"]
    password = request.form["password"]
    result = {
        "code": 500,
        "data": {}
    }

    try:
        user = auth.sign_in_with_email_and_password(email, password)
    except Exception:
        result["code"] = 403
        result["data"]["reason"] = "Invalid credentials."
        return make_response(jsonify(result), 200)

    session["user"] = user["idToken"]

    result["code"] = 200
    return make_response(jsonify(result), 200)

@app.route("/api/user/register", methods=["POST"])
def register():
    email = request.form["email"]
    password = request.form["password"]
    result = {
        "code": 500,
        "data": {}
    }

    try:
        user = auth.create_user_with_email_and_password(email, password)  
    except Exception:
        result["code"] = 403
        result["data"]["reason"] = "Access denied."
        return make_response(jsonify(result), 200)

    session["user"] = user["idToken"]

    result["code"] = 200
    return make_response(jsonify(result), 200)

@app.route("/api/user/status", methods=["POST"])
def status():
    result = { 
        "code": 500,
        "data": {}
    }

    if ("user" in session and session["user"] != None):
        try:
            user_info = auth.get_account_info(session["user"])
        except:
            result["code"] = 500
            result["data"]["reason"] = "Service unavailable."
            return make_response(jsonify(result), 200)

        result["code"] = 200
        result["data"]["userid"] = user_info["users"][0]["localId"]
        result["data"]["email"] = user_info["users"][0]["email"]
        result["data"]["emailVerified"] = user_info["users"][0]["emailVerified"]
        return make_response(jsonify(result), 200)
    else:
        result["code"] = 403
        result["data"]["reason"] = "Access denied."
        return make_response(jsonify(result), 200)

@app.route("/api/user/verifyemail", methods=["POST"])
def verifyEmail():
    result = { 
        "code": 500,
        "data": {}
    }

    if ("user" in session and session["user"] != None):
        try:
            user_info = auth.get_account_info(session["user"])
        except Exception:
            result["code"] = 500
            result["data"]["reason"] = "Service unavailable."
            return make_response(jsonify(result), 200)

        if (not user_info["users"][0]["emailVerified"]):
            try:
                auth.send_email_verification(session["user"])
            except Exception as ex:
                result["code"] = 403
                result["data"]["reason"] = "Access denied."
                return make_response(jsonify(result), 200)

            result["code"] = 200
            return make_response(jsonify(result), 200)
        else:
            result["code"] = 403
            result["data"]["reason"] = "Email already verified."
            return make_response(jsonify(result), 200)

    else:
        result["code"] = 403
        result["data"]["reason"] = "Access denied."
    return make_response(jsonify(result), 200)

@app.route("/api/user/signout", methods=["POST"])
def signout():
    result = { 
        "code": 200,
        "data": {}
    }

    session["user"] = None
    session.clear()

    return make_response(jsonify(result), 200)

if __name__ == "__main__":
    app.run(port=8081, use_reloader=True)
