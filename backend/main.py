#!/usr/bin/env python3

import json
import datetime
from flask import Flask, Response, jsonify, make_response, request, session
from flask_session import Session
from firebase_helper import firebase_helper
from utilities import call_api

fb = firebase_helper()

app = Flask("stocknews")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def set_session_user(data):
    session["user"] = {
        "localId": data["localId"],
        "idToken": data["idToken"],
        "expiry": datetime.datetime.now() +  + datetime.timedelta(0, int(data["expiresIn"]))
    }

def clear_session_user():
    session["user"] = None
    session.clear()

def is_session_user_set():
    return True if ("user" in session and session["user"] != None) else False

@app.route("/api/user/signin", methods=["POST"])
def signin() -> Response:
    email = request.form["email"]
    password = request.form["password"]
    response = {
        "code": "500",
        "data": {}
    }

    try:
        result = fb.verify_email_and_password(email, password)
    except RuntimeError:
        response["code"] = "403"
        response["data"]["reason"] = "Access denied."
        return make_response(jsonify(response), 200)
    except PermissionError:
        response["code"] = "403"
        response["data"]["reason"] = "Invalid credentials."
        return make_response(jsonify(response), 200)
    set_session_user(result)
    response["code"] = "200"
    return make_response(jsonify(response), 200)

@app.route("/api/user/register", methods=["POST"])
def register() -> Response:
    email = request.form["email"]
    password = request.form["password"]
    recaptcha_response = request.form["recaptcha_response"]
    response = {
        "code": "500",
        "data": {}
    }

    recaptcha_endpoint = "https://www.google.com/recaptcha/api/siteverify"
    recaptcha_data = {
        "secret": "6LeQ5LQkAAAAAFzmh3iSPp7-KyhSFzgcgXlxxmk2",
        "response": recaptcha_response,
        "remoteip": request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    }
    try:
        recaptcha_result = call_api(recaptcha_endpoint, recaptcha_data)
    except:
        response["code"] = "403"
        response["data"]["reason"] = "Access denied."
        return make_response(jsonify(response), 200)
    if not recaptcha_result["success"]:
        response["code"] = "403"
        response["data"]["reason"] = "Invalid reCAPTCHA response."
        return make_response(jsonify(response), 200)
    try:
        result = fb.sign_up_with_email_and_password(email, password)
    except RuntimeError:
        response["code"] = "403"
        response["data"]["reason"] = "Access denied."
        return make_response(jsonify(response), 200)
    except PermissionError as ex:
        ex_json = json.loads(str(ex))
        if ex_json["error"]["message"] == "EMAIL_EXISTS":
            response["code"] = "403"
            response["data"]["reason"] = "This email has already registered."
        else:
            response["code"] = "403"
            response["data"]["reason"] = "Access denied."
        return make_response(jsonify(response), 200)
    set_session_user(result)
    response["code"] = "200"
    return make_response(jsonify(response), 200)

@app.route("/api/user/status", methods=["POST"])
def status() -> Response:
    response = { 
        "code": "500",
        "data": {}
    }

    if is_session_user_set():
        try:
            result = fb.get_account_info(session["user"]["idToken"]) # TODO: check token expiry
        except:
            response["code"] = "403"
            response["data"]["reason"] = "Access denied."
            return make_response(jsonify(response), 200)
        response["code"] = "200"
        response["data"]["userid"] = result["users"][0]["localId"]
        response["data"]["email"] = result["users"][0]["email"]
        response["data"]["emailVerified"] = "true" if result["users"][0]["emailVerified"] else "false"
        return make_response(jsonify(response), 200)
    else:
        response["code"] = "403"
        response["data"]["reason"] = "Access denied."
        return make_response(jsonify(response), 200)

@app.route("/api/user/verifyemail", methods=["POST"])
def verifyEmail() -> Response:
    requestType = request.form["requestType"].lower()
    response = { 
        "code": "500",
        "data": {}
    }

    if requestType == "registration" or requestType == "reset_password":
        if is_session_user_set():
            if requestType == "registration":
                try:
                    result = fb.get_account_info(session["user"]["idToken"])
                except Exception:
                    response["code"] = "403"
                    response["data"]["reason"] = "Access denied."
                    return make_response(jsonify(response), 200)
                if (not result["users"][0]["emailVerified"]):
                    try:
                        fb.send_email_verification_email(session["user"]["idToken"])
                    except Exception:
                        response["code"] = "403"
                        response["data"]["reason"] = "Access denied."
                        return make_response(jsonify(response), 200)

                    response["code"] = "200"
                    return make_response(jsonify(response), 200)
                else:
                    response["code"] = "403"
                    response["data"]["reason"] = "Email already verified."
                    return make_response(jsonify(response), 200)
            elif requestType == "reset_password":
                print("reset password")
                response["code"] = "200"
                return make_response(jsonify(response), 200)
        else:
            response["code"] = "403"
            response["data"]["reason"] = "Access denied."
            return make_response(jsonify(response), 200)
    elif requestType == "sign_in":
        print("sign in")
        response["code"] = "200"
        return make_response(jsonify(response), 200)
    else:
        response["code"] = "403"
        response["data"]["reason"] = "Access denied."

@app.route("/api/user/resetpassword", methods=["POST"])
def resetPassword() -> Response:
    response = { 
        "code": "500",
        "data": {}
    }
        
    print("reset password")
    return make_response(jsonify(response), 200)

@app.route("/api/user/signout", methods=["POST"])
def signOut() -> Response:
    response = { 
        "code": "200",
        "data": {}
    }

    clear_session_user()
    return make_response(jsonify(response), 200)

if __name__ == "__main__":
    app.run(port=8081, use_reloader=True)
