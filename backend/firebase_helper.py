#!/usr/bin/env python3

import os, json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
import urllib
from utilities import call_api_post

script_path = os.path.realpath(os.path.dirname(__file__))

cred = credentials.Certificate(script_path + "/configs/stocknews-firebase-project.json")
conf = json.load(open(script_path + "/configs/stocknews-firebase-app.json"))

app = firebase_admin.initialize_app(cred)
auth = auth
db = firestore.client()

@staticmethod
def get_conf():
    return conf

@staticmethod
def get_app():
    return app

@staticmethod
def get_db():
    return db

@staticmethod
def get_auth():
    return auth

@staticmethod
def sign_up_with_email_and_password(email: str, password: str):
    endpoint = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={0}".format(conf["apiKey"])
    data = {"email": email, "password": password, "returnSecureToken": True}
    return call_api_post(endpoint, data)

@staticmethod
def verify_email_and_password(email: str, password: str):
    endpoint = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}".format(conf["apiKey"])
    data = {"email": email, "password": password, "returnSecureToken": True}
    return call_api_post(endpoint, data)

@staticmethod
def get_account_info(id_token: str):
    endpoint = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={0}".format(conf["apiKey"])
    data = {"idToken": id_token}
    return call_api_post(endpoint, data)

@staticmethod
def send_email_verification_email(idToken: str, email: str):
    endpoint = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(conf["apiKey"])
    data = {"requestType": "VERIFY_EMAIL", "idToken": idToken, "email": email }
    return call_api_post(endpoint, data)

@staticmethod
def send_email_sign_in_email(email: str):
    endpoint = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(conf["apiKey"])
    data = {"requestType": "EMAIL_SIGNIN", "email": email, "continueUrl": "http://localhost:8080/" + "emailsignin?" + urllib.parse.urlencode({"email": email})}
    return call_api_post(endpoint, data)

@staticmethod
def verify_email_sign_in_code(email: str, oobCode: str):
    endpoint = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/emailLinkSignin?key={0}".format(conf["apiKey"])
    data = {"email": email, "oobCode": oobCode}
    return call_api_post(endpoint, data)

@staticmethod
def send_password_reset_email(email: str):
    endpoint = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(conf["apiKey"])
    data = {"requestType": "PASSWORD_RESET", "email": email}
    return call_api_post(endpoint, data)

@staticmethod
def verify_password_reset_code(oobCode: str, newPassword: str):
    endpoint = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/resetPassword?key={0}".format(conf["apiKey"])
    data = {"oobCode": oobCode, "newPassword": newPassword}
    return call_api_post(endpoint, data)

@staticmethod
def update_account_info(localId: str, idToken: str, displayName: str):
    endpoint = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/setAccountInfo?key={0}".format(conf["apiKey"])
    data = {"localId": localId, "idToken": idToken, "displayName": displayName}
    return call_api_post(endpoint, data)

@staticmethod
def update_preferences(localId: str, algriculture: bool, mining: bool, construction: bool, manufacuring: bool, transportation: bool, wholesale: bool, retail: bool, finance: bool, services: bool, public_administration: bool):
    db.collection("user_preferences").document(localId).set({
        "agriculture": algriculture,
        "mining": mining,
        "construction": construction,
        "manufacturing": manufacuring,
        "transportation": transportation,
        "wholesale": wholesale,
        "retail": retail,
        "finance": finance,
        "services": services,
        "public_administration": public_administration
    })
    return True

@staticmethod
def get_preferences(localId: str):
    doc = db.collection("user_preferences").document(localId).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return {
            'agriculture': False,
            'mining': False,
            'construction': False,
            'manufacturing': False,
            'transportation': False,
            'wholesale': False,
            'retail': False,
            'finance': False,
            'services': False,
            'public_administration': False
        }

@staticmethod
def update_password(email: str, currentPassword: str, newPassword: str):
    endpoint = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/resetPassword?key={0}".format(conf["apiKey"])
    data = {"email": email, "oldPassword": currentPassword, "newPassword": newPassword}
    return call_api_post(endpoint, data)
