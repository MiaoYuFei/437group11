#!/usr/bin/env python3

import base64
import json
import requests
import mysql.connector

cnxconfig = {
    "host": "127.0.0.1",
    "user": "stocknews",
    "password": "Cse@437s",
    "database": "stocknews",
    "pool_size": 5
}
cnxpool = mysql.connector.pooling.MySQLConnectionPool(**cnxconfig)

@staticmethod
def call_api_post(endpoint, data):
    try:
        response = requests.post(endpoint, data=data, headers={
                                 "Referer": "https://cse437s.yufeim.com/api"})
    except Exception as ex:
        raise RuntimeError(json.dumps(ex))
    result = response.json()
    if "error" in result:
        raise PermissionError(json.dumps(result))
    return response.json()


@staticmethod
def call_api_get(endpoint, data):
    try:
        response = requests.get(endpoint, params=data, headers={
                                "Referer": "https://cse437s.yufeim.com/api"})
    except Exception as ex:
        raise RuntimeError(json.dumps(ex))
    result = response.json()
    if "error" in result:
        raise PermissionError(json.dumps(result))
    return response.json()

@staticmethod
def get_sql_connection():
    cnx = cnxpool.get_connection()
    if not cnx.is_connected():
        cnx.reconnect()
    return cnx

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

@staticmethod
def get_sic_category_code_from_sic_code(sic_code: str) -> str:
    if sic_code is None:
        return "N/A"
    if len(sic_code) < 2:
        return None
    sic_category = None
    if sic_code[0] == "0":
        sic_category = "agriculture"
    elif sic_code[0] == "1":
        sic_category = "mining"
    elif sic_code[0] == "2":
        sic_category = "construction"
    elif sic_code[0] == "3":
        sic_category = "manufacturing"
    elif sic_code[0] == "4":
        sic_category = "transportation"
    elif sic_code[0] == "5":
        sic_category = "wholesale"
    elif sic_code[0] == "6":
        sic_category = "retail"
    elif sic_code[0] == "7":
        sic_category = "finance"
    elif sic_code[0] == "8":
        sic_category = "services"
    elif sic_code[0] == "9":
        sic_category = "public_administration"
    return sic_category

@staticmethod
def get_sic_category_name_from_sic_category_code(sic_category_code: str) -> str:
    if sic_category_code == "agriculture":
        return "Agriculture, Forestry, Fishing and Hunting"
    elif sic_category_code == "mining":
        return "Mining, Quarrying, and Oil and Gas Extraction"
    elif sic_category_code == "construction":
        return "Construction"
    elif sic_category_code == "manufacturing":
        return "Manufacturing"
    elif sic_category_code == "transportation":
        return "Transportation and Warehousing"
    elif sic_category_code == "wholesale":
        return "Wholesale Trade"
    elif sic_category_code == "retail":
        return "Retail Trade"
    elif sic_category_code == "finance":
        return "Finance and Insurance"
    elif sic_category_code == "services":
        return "Services"
    elif sic_category_code == "public_administration":
        return "Public Administration"

@staticmethod
def get_string_base64_encoded(string: str) -> str:
    return base64.b64encode(string.encode("utf-8")).decode("utf-8")

def get_string_base64_decoded(string: str) -> str:
    return base64.b64decode(string.encode("utf-8")).decode("utf-8")
