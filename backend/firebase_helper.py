#!/usr/bin/env python3

import os, json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from utilities import call_api

script_path = os.path.realpath(os.path.dirname(__file__))

class firebase_helper:
    cred = credentials.Certificate(script_path + "/configs/stocknews-firebase-project.json")
    conf = json.load(open(script_path + "/configs/stocknews-firebase-app.json"))

    app = None
    auth = None
    db = None

    def __init__(self):
        self.app = firebase_admin.initialize_app(self.cred)
        self.auth = auth
        self.db = firestore.client()

    def get_conf(self):
        return self.conf

    def get_app(self):
        return self.app

    def get_db(self):
        return self.db

    def get_auth(self):
        return self.auth

    def sign_up_with_email_and_password(self, email, password):
        endpoint = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={0}".format(self.conf["apiKey"])
        data = {"email": email, "password": password, "returnSecureToken": True}
        return call_api(endpoint, data)

    def verify_email_and_password(self, email, password):
        endpoint = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}".format(self.conf["apiKey"])
        data = {"email": email, "password": password, "returnSecureToken": True}
        return call_api(endpoint, data)

    def get_account_info(self, id_token):
        endpoint = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={0}".format(self.conf["apiKey"])
        data = {"idToken": id_token}
        return call_api(endpoint, data)

    def send_email_verification_email(self, id_token):
        endpoint = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(self.conf["apiKey"])
        data = {"requestType": "VERIFY_EMAIL", "idToken": id_token}
        return call_api(endpoint, data)

    def send_password_reset_email(self, email):
        endpoint = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(self.conf["apiKey"])
        data = {"requestType": "PASSWORD_RESET", "email": email}
        return call_api(endpoint, data)

    def verify_password_reset_code(self, oob_code, new_password):
        endpoint = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/resetPassword?key={0}".format(self.conf["apiKey"])
        data = {"oobCode": oob_code, "newPassword": new_password}
        return call_api(endpoint, data)
