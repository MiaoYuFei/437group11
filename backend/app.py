#!/usr/bin/env python3

import json
import datetime
import urllib.parse
from flask import Flask, Response, jsonify, make_response, request, session
from flask_session import Session
from utilities import verify_recaptcha
from firebase_helper import firebase_helper
from stockdata_helper import stockdata_helper

fb = firebase_helper()
sd = stockdata_helper()

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
    responseData = {
        "code": "500",
        "data": {}
    }

    try:
        if requestType == "email_password":
            result = fb.verify_email_and_password(request.form["email"], request.form["password"])
        elif requestType == "email_link":
            result = fb.verify_email_sign_in_code(request.form["email"], request.form["oobCode"])
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
        result = fb.sign_up_with_email_and_password(email, password)
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
        fb.update_account_info(result["localId"], result["idToken"], name)
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
            result = fb.get_account_info(session["user"]["idToken"]) # TODO: check token expiry
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
                result = fb.get_account_info(session["user"]["idToken"])
            except Exception as ex:
                print(ex)
                responseData["code"] = "403"
                responseData["data"]["reason"] = "Access denied."
                return make_response(jsonify(responseData), 200)
            if (not result["users"][0]["emailVerified"]):
                try:
                    fb.send_email_verification_email(session["user"]["idToken"], session["user"]["email"])
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
            fb.send_email_sign_in_email(email)
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
            fb.send_password_reset_email(email)
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

@app.route("/api/user/update_account_info", methods=["POST"])
def update_account_info() -> Response:
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
        fb.update_account_info(localId, idToken, displayName)
    except Exception as ex:
        print(ex)
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)
    return make_response(jsonify(responseData), 200)

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
        fb.update_preferences(localId, algriculture, mining, construction, manufacuring, transportation, wholesale, retail, finance, services, public_administration)
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
        preferences = fb.get_preferences(session["user"]["localId"])
        responseData["data"]["preferences"] = preferences
    except Exception as ex:
        print(ex)
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
        fb.update_password(email, currentPassword, newPassword)
    except RuntimeError as ex:
        print(ex)
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
    return make_response(jsonify(responseData), 200)

@app.route("/api/news/getnews", methods=["POST"])
def getNews() -> Response:
    requestType = request.form["requestType"]
    responseData = {
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
        responseData["code"] = "403"
        responseData["data"]["news"] = "Invalid request type."
        return make_response(jsonify(responseData), 403)
    responseData["code"] = "200"
    responseData["data"]["news"] = temp
    return make_response(jsonify(responseData), 200)

@app.route("/api/stock/getprice", methods=["POST"])
def getPrice() -> Response:
    requestData = {
        "ticker": request.form["ticker"],
        "start_date": request.form["start_date"],
        "end_date": request.form["end_date"]
    }
    responseData = {
        "code": "200",
        "data": {}
    }

    try:
        result = sd.get_aggregates(requestData["ticker"], requestData["start_date"], requestData["end_date"])
    except Exception as ex:
        print(ex)
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
        result = sd.get_tickerinfo(requestData["ticker"])
    except Exception as ex:
        print(ex)
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)
    if result["status"].lower() != "ok":
        responseData["code"] = "404"
        responseData["data"]["reason"] = "No data found."
        return make_response(jsonify(responseData), 200)
    if "branding" in result["results"]:
        if "icon_url" in result["results"]["branding"]:
            result["results"]["branding"]["icon_url"] = "/api/polygon/proxy?url=" + urllib.parse.quote_plus(result["results"]["branding"]["icon_url"])
        if "logo_url" in result["results"]["branding"]:
            result["results"]["branding"]["logo_url"] = "/api/polygon/proxy?url=" + urllib.parse.quote_plus(result["results"]["branding"]["logo_url"])

    responseData["code"] = "200"
    responseData["data"] = result["results"]

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
        result = sd.proxy_polygon_resource(requestData["url"])
    except Exception as ex:
        print(ex)
        responseData["code"] = "403"
        responseData["data"]["reason"] = "Access denied."
        return make_response(jsonify(responseData), 200)
    headers = result["headers"]
    data = result["data"]
    responseObj = make_response(data, 200)
    for key, value in headers.items():
        responseObj.headers[key] = value
    return responseObj

if __name__ == "__main__":
    app.run(port=8081, use_reloader=True)
