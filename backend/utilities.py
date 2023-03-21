#!/usr/bin/env python3

import json, requests

@staticmethod
def call_api_post(endpoint, data):
    try:
        response = requests.post(endpoint, data=data, headers={"Referer": "https://cse437s.yufeim.com/api"})
    except Exception as ex:
        raise RuntimeError(json.dumps(ex))
    result = response.json()
    if "error" in result:
        raise PermissionError(json.dumps(result))
    return response.json()

@staticmethod
def call_api_get(endpoint, data):
    try:
        response = requests.get(endpoint, params=data, headers={"Referer": "https://cse437s.yufeim.com/api"})
    except Exception as ex:
        raise RuntimeError(json.dumps(ex))
    result = response.json()
    if "error" in result:
        raise PermissionError(json.dumps(result))
    return response.json()

@staticmethod
def verify_recaptcha(recaptcha_response: str, remote_ip: str):
    recaptcha_endpoint = "https://www.google.com/recaptcha/api/siteverify"
    recaptcha_data = {
        "secret": "6LeQ5LQkAAAAAFzmh3iSPp7-KyhSFzgcgXlxxmk2",
        "response": recaptcha_response,
        "remoteip": remote_ip
    }
    try:
        recaptcha_result = call_api_post(recaptcha_endpoint, recaptcha_data)
    except Exception as ex:
        print(ex)
        return False
    if not recaptcha_result["success"]:
        return False
    return True
