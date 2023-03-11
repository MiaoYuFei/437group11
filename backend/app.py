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
        "email": data["email"],
        "expiry": datetime.datetime.now() +  + datetime.timedelta(0, int(data["expiresIn"]))
    }

def clear_session_user():
    session["user"] = None
    session.clear()

def is_session_user_set():
    return True if ("user" in session and session["user"] != None) else False

@app.route("/api/user/signin", methods=["POST"])
def signin() -> Response:
    requestType = request.form["requestType"].lower()
    response = {
        "code": "500",
        "data": {}
    }

    try:
        if requestType == "email_password":
            result = fb.verify_email_and_password(request.form["email"], request.form["password"])
        elif requestType == "email_link":
            result = fb.verify_email_sign_in_code(request.form["email"], request.form["oobCode"])
        else:
            response["code"] = "403"
            response["data"]["reason"] = "Sign in type not supported."
            return make_response(jsonify(response), 200)
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
    except Exception as ex:
        print(ex)
        response["code"] = "403"
        response["data"]["reason"] = "Access denied."
        return make_response(jsonify(response), 200)
    if not recaptcha_result["success"]:
        response["code"] = "403"
        response["data"]["reason"] = "Invalid reCAPTCHA response."
        return make_response(jsonify(response), 200)
    try:
        result = fb.sign_up_with_email_and_password(email, password)
    except RuntimeError as ex:
        print(ex)
        response["code"] = "403"
        response["data"]["reason"] = "Access denied."
        return make_response(jsonify(response), 200)
    except PermissionError as ex:
        ex_json = json.loads(str(ex))
        if ex_json["error"]["message"] == "EMAIL_EXISTS":
            response["code"] = "403"
            response["data"]["reason"] = "This email has already registered."
        else:
            print(ex)
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
        user = result["users"][0]
        response["data"]["id"] = user["localId"]
        if "displayName" in user:
            response["data"]["name"] = user["displayName"]
        else:
            response["data"]["name"] = user["email"]
        response["data"]["email"] = user["email"]
        response["data"]["emailVerified"] = "true" if user["emailVerified"] else "false"
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

    if requestType == "registration":
        if is_session_user_set():
            try:
                result = fb.get_account_info(session["user"]["idToken"])
            except Exception as ex:
                print(ex)
                response["code"] = "403"
                response["data"]["reason"] = "Access denied."
                return make_response(jsonify(response), 200)
            if (not result["users"][0]["emailVerified"]):
                try:
                    fb.send_email_verification_email(session["user"]["idToken"], session["user"]["email"])
                except Exception as ex:
                    print(ex)
                    response["code"] = "403"
                    response["data"]["reason"] = "Access denied."
                    return make_response(jsonify(response), 200)
                response["code"] = "200"
                return make_response(jsonify(response), 200)
            else:
                response["code"] = "403"
                response["data"]["reason"] = "Email already verified."
                return make_response(jsonify(response), 200)
        else:
            response["code"] = "403"
            response["data"]["reason"] = "Access denied."
            return make_response(jsonify(response), 200)
    elif requestType == "sign_in":
        email = request.form["email"]
        try:
            fb.send_email_sign_in_email(email)
        except Exception as ex:
            ex_json = json.loads(str(ex))
            if ex_json["error"]["message"].upper().startswith("QUOTA_EXCEEDED"):
                response["code"] = "403"
                response["data"]["reason"] = "Firebase refused email sign in: Quota (5/day) exceeded."
            else:
                print(ex)
                response["code"] = "403"
                response["data"]["reason"] = "Access denied."
            return make_response(jsonify(response), 200)
        response["code"] = "200"
        return make_response(jsonify(response), 200)
    elif requestType == "reset_password":
        email = request.form["email"]
        try:
            fb.send_password_reset_email(email)
        except RuntimeError:
            response["code"] = "403"
            response["data"]["reason"] = "Access denied."
            return make_response(jsonify(response), 200)
        except PermissionError as ex:
            ex_json = json.loads(str(ex)) # TODO: This is not safe. Consider add custom Exception class
            if ex_json["error"]["message"].upper().startswith("EMAIL_NOT_FOUND"):
                response["code"] = "200"
            elif ex_json["error"]["message"] == "INVALID_EMAIL":
                response["code"] = "403"
                response["data"]["reason"] = "This email is invalid."
            else:
                response["code"] = "403"
                response["data"]["reason"] = "Access denied."
            return make_response(jsonify(response), 200)
        response["code"] = "200"
        return make_response(jsonify(response), 200)
    else:
        response["code"] = "403"
        response["data"]["reason"] = "Access denied."

@app.route("/api/user/signout", methods=["POST"])
def signOut() -> Response:
    response = { 
        "code": "200",
        "data": {}
    }

    clear_session_user()
    return make_response(jsonify(response), 200)

@app.route("/api/user/update_account_info", methods=["POST"])
def update_account_info() -> Response:
    displayName = request.form["displayName"].strip()
    response = {
        "code": "200",
        "data": {}
    }

    if not is_session_user_set():
        response["code"] = "403"
        response["data"]["reason"] = "Access denied."
        return make_response(jsonify(response), 200)

    localId = session["user"]["localId"]
    idToken = session["user"]["idToken"]
    try:
        fb.update_account_info(localId, idToken, displayName)
    except RuntimeError as ex:
        print(ex)
        response["code"] = "403"
        response["data"]["reason"] = "Access denied."
        return make_response(jsonify(response), 200)
    return make_response(jsonify(response), 200)

@app.route("/api/user/updatepreferences", methods=["POST"])
def updatePreferences() -> Response:
    algriculture = request.form["algriculture"].lower()
    mining = request.form["mining"].lower()
    construction = request.form["construction"].lower()
    manufacuring = request.form["manufacuring"].lower()
    transportation = request.form["transportation"].lower()
    wholesale = request.form["wholesale"].lower()
    retail = request.form["retail"].lower()
    finance = request.form["finance"].lower()
    services = request.form["services"].lower()
    public_administration = request.form["public_administration"].lower()
    response = { 
        "code": "500",
        "data": {}
    }

    if not is_session_user_set():
        response["code"] = "403"
        response["data"]["reason"] = "Access denied."
        return make_response(jsonify(response), 200)
    
    localId = session["user"]["localId"]
    try:
        fb.update_preferences(localId, algriculture, mining, construction, manufacuring, transportation, wholesale, retail, finance, services, public_administration)
    except Exception as ex:
        print(ex)
        response["code"] = "403"
        response["data"]["reason"] = "Access denied."
        return make_response(jsonify(response), 200)
    
    response["code"] = "200"
    return make_response(jsonify(response), 200)

@app.route("/api/user/getpreferences", methods=["POST"])
def getPreferences() -> Response:
    response = { 
        "code": "500",
        "data": {}
    }

    if not is_session_user_set():
        response["code"] = "403"
        response["data"]["reason"] = "Access denied."
        return make_response(jsonify(response), 200)

    try:
        preferences = fb.get_preferences(session["user"]["localId"])
        response["data"]["preferences"] = preferences
    except Exception as ex:
        print(ex)
        response["code"] = "403"
        response["data"]["reason"] = "Access denied."
        return make_response(jsonify(response), 200)

    response["code"] = "200"
    return make_response(jsonify(response), 200)

@app.route("/api/user/updatepassword", methods=["POST"])
def updatePassword() -> Response:
    currentPassword = request.form["currentPassword"]
    newPassword = request.form["newPassword"]
    response = {
        "code": "500",
        "data": {}
    }

    if not is_session_user_set():
        response["code"] = "403"
        response["data"]["reason"] = "Access denied."
        return make_response(jsonify(response), 200)
    
    email = session["user"]["email"]
    try:
        fb.update_password(email, currentPassword, newPassword)
    except RuntimeError as ex:
        print(ex)
        response["code"] = "403"
        response["data"]["reason"] = "Access denied."
        return make_response(jsonify(response), 200)
    except PermissionError as ex:
        ex_json = json.loads(str(ex))
        if ex_json["error"]["message"].upper().startswith("INVALID_PASSWORD"):
            response["code"] = "403"
            response["data"]["reason"] = "Invalid current password."
            return make_response(jsonify(response), 200)
    response["code"] = "200"
    return make_response(jsonify(response), 200)

@app.route("/api/news/getnews", methods=["POST"])
def getNews() -> Response:
    requestType = request.form["requestType"]
    response = {
        "code": "500",
        "data": {}
    }

    temp = []

    if requestType == "recommendations":
        temp = [ \
        {"article": {"title": "Invest Like Warren Buffett, Not Carl Icahn", "description": "Warren Buffett and Carl Icahn are two of the most successful investors of the past century. But Buffett is a superior model for investors to follow because of his patient style and focus on finding great businesses.", "keywords": ["investing"], "datetime": "2017-04-10T00:24:00Z", "url": "https://www.fool.com/investing/2017/04/09/invest-like-warren-buffett-not-carl-icahn.aspx"}, "cover_image": {"url": "https://g.foolcdn.com/editorial/images/435736/warren-buffett3_tmf.jpg"}, "publisher": {"name": "The Motley Fool", "homepage": {"url": "https://www.fool.com/"}, "logo": {"url": "https://s3.polygon.io/public/assets/news/logos/themotleyfool.svg"}}, "tickers": ["BRK.B", "IEP", "BRK.A", "AAPL", "NFLX"]}, \
        {"article": {"title": "Should Apple Investors Believe Tim Cook\'s Promise of Innovation?", "description": "There are nearly 15 billion reasons to do so.", "keywords": ["investing"], "datetime": "2019-03-05T11:03:00Z", "url": "https://www.fool.com/investing/2019/03/05/should-apple-investors-believe-tim-cooks-promise-o.aspx"}, "cover_image": {"url": "https://g.foolcdn.com/editorial/images/514902/apple-keynote-tim-cook-september-event-09122018.jpg"}, "publisher": {"name": "The Motley Fool", "homepage": {"url": "https://www.fool.com/"}, "logo": {"url": "https://s3.polygon.io/public/assets/news/logos/themotleyfool.svg"}}, "tickers": ["AAPL"]}, \
        {"article": {"title": "Apple Is Going to Be Late to 5G -- So What?", "description": "Apple won\'t be the first to adopt this new wireless technology, but that doesn\'t mean the company will be completely helpless.", "keywords": ["investing"], "datetime": "2019-03-03T13:15:00Z", "url": "https://www.fool.com/investing/2019/03/03/apple-is-going-to-be-late-to-5g-so-what.aspx"}, "cover_image": {"url": "https://g.foolcdn.com/editorial/images/514453/apple-customer.jpg"}, "publisher": {"name": "The Motley Fool", "homepage": {"url": "https://www.fool.com/"}, "logo": {"url": "https://s3.polygon.io/public/assets/news/logos/themotleyfool.svg"}}, "tickers": ["AAPL"]}]
    elif requestType == "myfavorites":
        temp = [ \
        {"article": {"title": "MY: Invest Like Warren Buffett, Not Carl Icahn", "description": "Warren Buffett and Carl Icahn are two of the most successful investors of the past century. But Buffett is a superior model for investors to follow because of his patient style and focus on finding great businesses.", "keywords": ["investing"], "datetime": "2017-04-10T00:24:00Z", "url": "https://www.fool.com/investing/2017/04/09/invest-like-warren-buffett-not-carl-icahn.aspx"}, "cover_image": {"url": "https://g.foolcdn.com/editorial/images/435736/warren-buffett3_tmf.jpg"}, "publisher": {"name": "The Motley Fool", "homepage": {"url": "https://www.fool.com/"}, "logo": {"url": "https://s3.polygon.io/public/assets/news/logos/themotleyfool.svg"}}, "tickers": ["BRK.B", "IEP", "BRK.A", "AAPL", "NFLX"]}, \
        {"article": {"title": "MY: Should Apple Investors Believe Tim Cook\'s Promise of Innovation?", "description": "There are nearly 15 billion reasons to do so.", "keywords": ["investing"], "datetime": "2019-03-05T11:03:00Z", "url": "https://www.fool.com/investing/2019/03/05/should-apple-investors-believe-tim-cooks-promise-o.aspx"}, "cover_image": {"url": "https://g.foolcdn.com/editorial/images/514902/apple-keynote-tim-cook-september-event-09122018.jpg"}, "publisher": {"name": "The Motley Fool", "homepage": {"url": "https://www.fool.com/"}, "logo": {"url": "https://s3.polygon.io/public/assets/news/logos/themotleyfool.svg"}}, "tickers": ["AAPL"]}, \
        {"article": {"title": "MY: Apple Is Going to Be Late to 5G -- So What?", "description": "Apple won\'t be the first to adopt this new wireless technology, but that doesn\'t mean the company will be completely helpless.", "keywords": ["investing"], "datetime": "2019-03-03T13:15:00Z", "url": "https://www.fool.com/investing/2019/03/03/apple-is-going-to-be-late-to-5g-so-what.aspx"}, "cover_image": {"url": "https://g.foolcdn.com/editorial/images/514453/apple-customer.jpg"}, "publisher": {"name": "The Motley Fool", "homepage": {"url": "https://www.fool.com/"}, "logo": {"url": "https://s3.polygon.io/public/assets/news/logos/themotleyfool.svg"}}, "tickers": ["AAPL"]}]
    else:
        response["code"] = "403"
        response["data"]["news"] = "Invalid request type."
        return make_response(jsonify(response), 403)
    response["code"] = "200"
    response["data"]["news"] = temp
    return make_response(jsonify(response), 200)

if __name__ == "__main__":
    app.run(port=8081, use_reloader=True)
