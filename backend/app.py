#!/usr/bin/env python3

import datetime
from flask import Flask, Response, jsonify, make_response, request, session
from flask_session import Session
import json
import logging
import urllib.parse

import firebase_helper
from newsdata_helper import newsdata_helper
from stockdata_helper import stockdata_helper
from utilities import get_sic_category_code_from_sic_code, verify_recaptcha

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

app = Flask("stocknews")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def set_session_user(data):
    session["user"] = {
        "localId": data["localId"],
        "idToken": data["idToken"],
        "email": data["email"],
        "expiry": datetime.datetime.utcnow() +  + datetime.timedelta(0, int(data["expiresIn"]))
    }

def clear_session_user():
    session["user"] = None
    session.clear()

def is_session_user_set():
    if "user" in session and session["user"] != None:
        if "expiry" in session["user"] and session["user"]["expiry"] < datetime.datetime.utcnow():
            clear_session_user()
            return False
        else:
            return True
    else:
        return False

@app.route("/api/user/signin", methods=["POST"])
def signin() -> Response:
    requestType = request.form["requestType"].lower()
    responseData = {
        "code": "500",
        "data": {}
    }

    try:
        if requestType == "email_password":
            result = firebase_helper.verify_email_and_password(request.form["email"], request.form["password"])
        elif requestType == "email_link":
            result = firebase_helper.verify_email_sign_in_code(request.form["email"], request.form["oobCode"])
        else:
            responseData["code"] = "403"
            responseData["data"]["reason"] = "Sign in type not supported."
            return make_response(jsonify(responseData), 200)
    except RuntimeError:
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)
    except PermissionError:
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Invalid credentials."
        return make_response(jsonify(responseData), 200)
    set_session_user(result)
    responseData["code"] = "200"
    return make_response(jsonify(responseData), 200)

@app.route("/api/user/register", methods=["POST"])
def register() -> Response:
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    recaptcha_response = request.form["recaptchaResponse"]
    responseData = {
        "code": "500",
        "data": {}
    }

    if not verify_recaptcha(recaptcha_response, request.environ.get('HTTP_X_REAL_IP', request.remote_addr)):
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Invalid reCAPTCHA response."
        return make_response(jsonify(responseData), 200)

    try:
        result = firebase_helper.sign_up_with_email_and_password(email, password)
    except RuntimeError as ex:
        print(ex)
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)
    except PermissionError as ex:
        ex_json = json.loads(str(ex))
        if ex_json["error"]["message"] == "EMAIL_EXISTS":
            responseData["code"] = "403"
            responseData["data"]["reason"] = "This email has already registered."
        else:
            print(ex)
            responseData["code"] = "403"
            responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)
    set_session_user(result)
    try:
        firebase_helper.update_account_info(result["localId"], result["idToken"], name)
    except Exception:
        print(ex)
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)
    responseData["code"] = "200"
    return make_response(jsonify(responseData), 200)

@app.route("/api/user/status", methods=["POST"])
def status() -> Response:
    responseData = { 
        "code": "500",
        "data": {}
    }

    if is_session_user_set():
        try:
            result = firebase_helper.get_account_info(session["user"]["idToken"]) # TODO: check token expiry
        except:
            responseData["code"] = "403"
            responseData["data"]["reason"] = "Access denied."
            return make_response(jsonify(responseData), 200)
        responseData["code"] = "200"
        user = result["users"][0]
        responseData["data"]["id"] = user["localId"]
        if "displayName" in user:
            responseData["data"]["name"] = user["displayName"]
        else:
            responseData["data"]["name"] = user["email"]
        responseData["data"]["email"] = user["email"]
        responseData["data"]["emailVerified"] = "true" if user["emailVerified"] else "false"
        return make_response(jsonify(responseData), 200)
    else:
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)

@app.route("/api/user/verifyemail", methods=["POST"])
def verifyEmail() -> Response:
    requestType = request.form["requestType"].lower()
    responseData = { 
        "code": "500",
        "data": {}
    }

    if requestType == "registration":
        if is_session_user_set():
            try:
                result = firebase_helper.get_account_info(session["user"]["idToken"])
            except Exception as ex:
                print(ex)
                responseData["code"] = "403"
                responseData["data"]["reason"] = "Access denied."
                return make_response(jsonify(responseData), 200)
            if (not result["users"][0]["emailVerified"]):
                try:
                    firebase_helper.send_email_verification_email(session["user"]["idToken"], session["user"]["email"])
                except Exception as ex:
                    print(ex)
                    responseData["code"] = "403"
                    responseData["data"]["reason"] = "Access denied."
                    return make_response(jsonify(responseData), 200)
                responseData["code"] = "200"
                return make_response(jsonify(responseData), 200)
            else:
                responseData["code"] = "403"
                responseData["data"]["reason"] = "Email already verified."
                return make_response(jsonify(responseData), 200)
        else:
            responseData["code"] = "403"
            responseData["data"]["reason"] = "Access denied."
            return make_response(jsonify(responseData), 200)
    elif requestType == "sign_in":
        email = request.form["email"]
        try:
            firebase_helper.send_email_sign_in_email(email)
        except Exception as ex:
            ex_json = json.loads(str(ex))
            if ex_json["error"]["message"].upper().startswith("QUOTA_EXCEEDED"):
                responseData["code"] = "403"
                responseData["data"]["reason"] = "Firebase refused email sign in: Quota (5/day) exceeded."
            else:
                print(ex)
                responseData["code"] = "403"
                responseData["data"]["reason"] = "Access denied."
            return make_response(jsonify(responseData), 200)
        responseData["code"] = "200"
        return make_response(jsonify(responseData), 200)
    elif requestType == "reset_password":
        email = request.form["email"]
        try:
            firebase_helper.send_password_reset_email(email)
        except RuntimeError:
            responseData["code"] = "403"
            responseData["data"]["reason"] = "Access denied."
            return make_response(jsonify(responseData), 200)
        except PermissionError as ex:
            ex_json = json.loads(str(ex)) # TODO: This is not safe. Consider add custom Exception class
            if ex_json["error"]["message"].upper().startswith("EMAIL_NOT_FOUND"):
                responseData["code"] = "200"
            elif ex_json["error"]["message"] == "INVALID_EMAIL":
                responseData["code"] = "403"
                responseData["data"]["reason"] = "This email is invalid."
            else:
                responseData["code"] = "403"
                responseData["data"]["reason"] = "Access denied."
            return make_response(jsonify(responseData), 200)
        responseData["code"] = "200"
        return make_response(jsonify(responseData), 200)
    else:
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."

@app.route("/api/user/signout", methods=["POST"])
def signOut() -> Response:
    responseData = { 
        "code": "200",
        "data": {}
    }

    clear_session_user()
    return make_response(jsonify(responseData), 200)

@app.route("/api/user/updateaccountinfo", methods=["POST"])
def updateAccountInfo() -> Response:
    displayName = request.form["displayName"].strip()
    responseData = {
        "code": "200",
        "data": {}
    }

    if not is_session_user_set():
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)
    localId = session["user"]["localId"]
    idToken = session["user"]["idToken"]
    try:
        firebase_helper.update_account_info(localId, idToken, displayName)
    except Exception as ex:
        print(ex)
        logging.error(ex)
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)
    return make_response(jsonify(responseData), 200)

@app.route("/api/user/updatepreferences", methods=["POST"])
def updatePreferences() -> Response:
    agriculture = request.form["agriculture"].lower()
    mining = request.form["mining"].lower()
    construction = request.form["construction"].lower()
    manufacturing = request.form["manufacturing"].lower()
    transportation = request.form["transportation"].lower()
    wholesale = request.form["wholesale"].lower()
    retail = request.form["retail"].lower()
    finance = request.form["finance"].lower()
    services = request.form["services"].lower()
    public_administration = request.form["public_administration"].lower()
    responseData = { 
        "code": "500",
        "data": {}
    }

    if not is_session_user_set():
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)
    localId = session["user"]["localId"]
    try:
        firebase_helper.update_preferences(localId, agriculture, mining, construction, manufacturing, transportation, wholesale, retail, finance, services, public_administration)
    except Exception as ex:
        print(ex)
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)
    
    responseData["code"] = "200"
    return make_response(jsonify(responseData), 200)

@app.route("/api/user/getpreferences", methods=["POST"])
def getPreferences() -> Response:
    responseData = { 
        "code": "500",
        "data": {}
    }

    if not is_session_user_set():
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)
    try:
        preferences = firebase_helper.get_preferences(session["user"]["localId"])
        responseData["data"]["preferences"] = preferences
    except Exception as ex:
        print(ex)
        logging.error(ex)
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)

    responseData["code"] = "200"
    return make_response(jsonify(responseData), 200)

@app.route("/api/user/updatepassword", methods=["POST"])
def updatePassword() -> Response:
    currentPassword = request.form["currentPassword"]
    newPassword = request.form["newPassword"]
    recaptcha_response = request.form["recaptchaResponse"]
    responseData = {
        "code": "500",
        "data": {}
    }

    if not verify_recaptcha(recaptcha_response, request.environ.get('HTTP_X_REAL_IP', request.remote_addr)):
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Invalid reCAPTCHA response."
        return make_response(jsonify(responseData), 200)

    if not is_session_user_set():
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)
    email = session["user"]["email"]
    try:
        firebase_helper.update_password(email, currentPassword, newPassword)
    except RuntimeError as ex:
        print(ex)
        logging.error(ex)
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)
    except PermissionError as ex:
        ex_json = json.loads(str(ex))
        if ex_json["error"]["message"].upper().startswith("INVALID_PASSWORD"):
            responseData["code"] = "403"
            responseData["data"]["reason"] = "Invalid current password."
            return make_response(jsonify(responseData), 200)
    responseData["code"] = "200"
    clear_session_user()

    return make_response(jsonify(responseData), 200)

@app.route("/api/stock/gettickerinfo", methods=["POST"])
def getTickerInfo() -> Response:
    requestData = {
        "ticker": request.form["ticker"]
    }
    responseData = {
        "code": "200",
        "data": {}
    }

    try:
        result1 = stockdata_helper.get_tickerinfo(requestData["ticker"])
    except Exception as ex:
        print(ex)
        logging.error(ex)
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)
    if result1["status"].lower() != "ok":
        responseData["code"] = "404"
        responseData["data"]["reason"] = "Ticker not found."
        return make_response(jsonify(responseData), 200)

    result = result1["results"]

    try:
        result2 = stockdata_helper.get_last_trading_date(requestData["ticker"])
    except Exception as ex:
        print(ex)
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)

    result["last_trading_date"] = datetime.datetime.utcfromtimestamp(
        int(result2["results"]["t"] / 1000000000)
        ).strftime("%Y-%m-%d")

    if "branding" in result:
        if "icon_url" in result["branding"] and result["branding"]["icon_url"] is not None:
            result["branding"]["icon_url"] = "/api/polygon/proxy?url=" + urllib.parse.quote_plus(result["branding"]["icon_url"])
        if "logo_url" in result["branding"] and result["branding"]["logo_url"] is not None:
            result["branding"]["logo_url"] = "/api/polygon/proxy?url=" + urllib.parse.quote_plus(result["branding"]["logo_url"])
    result["category"] = get_sic_category_code_from_sic_code(result["sic_code"])

    responseData["code"] = "200"
    responseData["data"] = result

    return make_response(jsonify(responseData), 200)

@app.route("/api/stock/getprice", methods=["POST"])
def getPrice() -> Response:
    requestData = {
        "ticker": request.form["ticker"],
        "start_date": request.form["start_date"],
        "end_date": request.form["end_date"],
        "mode": request.form["mode"]
    }
    responseData = {
        "code": "200",
        "data": {}
    }

    try:
        result = stockdata_helper.get_aggregates(requestData["ticker"], requestData["start_date"], requestData["end_date"], requestData["mode"])
    except Exception as ex:
        print(ex)
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)
    
    if result["status"].lower() != "ok":
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)

    if result["resultsCount"] <= 0:
        responseData["code"] = "404"
        responseData["data"]["reason"] = "No data found."
        return make_response(jsonify(responseData), 200)
    responseData["code"] = "200"
    responseData["data"]["price"] = []
    for item in result["results"]:
        responseData["data"]["price"].append({"open": item["o"], "close": item["c"], "low": item["l"], "high": item["h"], "timestamp": item["t"]})
    
    return make_response(jsonify(responseData), 200)

@app.route("/api/polygon/proxy", methods=["GET"])
def proxyPolygon() -> Response:
    requestData = {
        "url": request.args.get("url")
    }
    responseData = {
        "code": "200",
        "data": {}
    }

    try:
        result = stockdata_helper.proxy_polygon_resource(requestData["url"])
    except Exception as ex:
        print(ex)
        logging.error(ex)
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)
    headers = result["headers"]
    data = result["data"]
    responseObj = make_response(data, 200)
    for key, value in headers.items():
        responseObj.headers[key] = value
    return responseObj

@app.route("/api/news/setnewsuseraction", methods=["POST"])
def setNewsUserAction() -> Response:
    requestData = {
        "requestType": request.form["requestType"],
        "newsId": request.form["newsId"],
    }
    responseData = {
        "code": "200",
        "data": {}
    }

    if not is_session_user_set():
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)

    requestData["userId"] = session["user"]["localId"]
    if requestData["requestType"].lower() == "like":
        requestData["liked"] = request.form["liked"].lower() == "true" or request.form["liked"] == "1"
    elif requestData["requestType"].lower() == "collect":
        requestData["collected"] = request.form["collected"].lower() == "true" or request.form["collected"] == "1"
    try:
        if requestData["requestType"].lower() == "like":
            newsdata_helper.set_user_news_like(requestData["newsId"], requestData["userId"], requestData["liked"])
        elif requestData["requestType"].lower() == "collect":
            newsdata_helper.set_user_news_collect(requestData["newsId"], requestData["userId"], requestData["collected"])
    except Exception as ex:
        print(ex)
        logging.error(ex)
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)
    responseData["code"] = "200"

    return make_response(jsonify(responseData), 200)

@app.route("/api/news/getnews", methods=["POST"])
def getNews() -> Response:
    requestData = {
        "requestType": request.form["requestType"].lower()
    }
    if "page" in request.form:
        requestData["offset"] = (int(request.form["page"]) - 1) * 10
    else:
        requestData["offset"] = 0
    responseData = {
        "code": "200",
        "data": {}
    }

    if requestData["requestType"] in ["recommendation", "collection"]:
        if not is_session_user_set():
            responseData["code"] = "403"
            responseData["data"]["reason"] = "Access denied."
            return make_response(jsonify(responseData), 200)

    if is_session_user_set():
        requestData["userId"] = session["user"]["localId"]
    else:
        requestData["userId"] = None

    result = []

    try:
        if requestData["requestType"] == "latest":
            result = newsdata_helper.get_news_latest(requestData["userId"], requestData["offset"])
        elif requestData["requestType"] == "search":
            result = newsdata_helper.search_news(request.form["q"], requestData["userId"], requestData["offset"])
        elif requestData["requestType"] == "ticker":
            result = newsdata_helper.get_news_by_ticker(request.form["ticker"], requestData["userId"], requestData["offset"])
        elif requestData["requestType"] == "category":
            result = newsdata_helper.get_news_by_category(request.form["category"], requestData["userId"], requestData["offset"])
        elif requestData["requestType"] == "recommendation":
            result = newsdata_helper.get_user_news_recommendation(requestData["userId"], requestData["offset"])
        elif requestData["requestType"] == "collection":
            result = newsdata_helper.get_user_news_collection(requestData["userId"], requestData["offset"])
    except Exception as ex:
        print(ex)
        logging.error(ex)
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)

    responseData["code"] = "200"
    responseData["data"] = result

    return make_response(jsonify(responseData), 200)

if __name__ == "__main__":
    app.run(port=8081, use_reloader=True)
