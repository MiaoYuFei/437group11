#!/usr/bin/env python3

import base64
import json
import mysql.connector
import os
import platform
import requests

if os.name == "nt":
    cnxconfig = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "stocknews",
        "password": "Cse@437s",
        "database": "stocknews",
        "pool_size": 32
    }
elif platform.system() == "Darwin":
    cnxconfig = {
        "unix_socket": "/tmp/mysql.sock",
        "user": "stocknews",
        "password": "Cse@437s",
        "database": "stocknews",
        "pool_size": 32
    }
else:
    cnxconfig = {
        "unix_socket": "/var/run/mysqld/mysqld.sock",
        "user": "stocknews",
        "password": "Cse@437s",
        "database": "stocknews",
        "pool_size": 32
    }

cnxpool = mysql.connector.pooling.MySQLConnectionPool(**cnxconfig)

@staticmethod
def call_api_post(endpoint, data):
    try:
        response = requests.post(endpoint, data=data,
                                 headers={"Referer": "https://cse437s.yufeim.com/api"})
    except Exception as ex:
        raise RuntimeError(json.dumps(ex))
    result = response.json()
    if "error" in result:
        raise PermissionError(json.dumps(result))
    return response.json()


@staticmethod
def call_api_get(endpoint, data):
    try:
        response = requests.get(endpoint, params=data,
                                headers={"Referer": "https://cse437s.yufeim.com/api"})
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
    sic_code_number = int(sic_code[0:2])
    if sic_code_number >= 0 and sic_code_number <= 9:
        sic_category = "agriculture"
    elif sic_code_number >= 10 and sic_code_number <= 14:
        sic_category = "mining"
    elif sic_code_number >= 15 and sic_code_number <= 17:
        sic_category = "construction"
    elif sic_code_number >= 20 and sic_code_number <= 39:
        sic_category = "manufacturing"
    elif sic_code_number >= 40 and sic_code_number <= 49:
        sic_category = "transportation"
    elif sic_code_number >= 50 and sic_code_number <= 51:
        sic_category = "wholesale"
    elif sic_code_number >= 52 and sic_code_number <= 59:
        sic_category = "retail"
    elif sic_code_number >= 60 and sic_code_number <= 67:
        sic_category = "finance"
    elif sic_code_number >= 70 and sic_code_number <= 89:
        sic_category = "services"
    elif sic_code_number >= 91 and sic_code_number <= 99:
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
