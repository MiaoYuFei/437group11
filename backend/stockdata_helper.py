#!/usr/bin/env python3

import os

import requests

from utilities import get_string_base64_encoded, get_sql_connection, call_api_get

script_path = os.path.realpath(os.path.dirname(__file__))

api_key = "GNthmWT9qYGm57QwnIJ_orim_uN5mbc0"

class stockdata_helper:

    @staticmethod
    def get_aggregates(ticker: str, start_date: str, end_date: str, mode: str):
        endpoint = "https://api.polygon.io/v2/aggs/ticker/{0}/range/1/{1}/{2}/{3}".format(ticker, mode, start_date, end_date)
        requestData = {"apiKey": api_key, "adjusted": "true", "sort": "desc", "limit": "1000"}
        return call_api_get(endpoint, requestData)

    @staticmethod
    def get_last_trading_date(ticker: str):
        endpoint = "https://api.polygon.io/v2/last/trade/{0}".format(ticker)
        requestData = {"apiKey": api_key, "stocksTicker": ticker}
        return call_api_get(endpoint, requestData)

    @staticmethod
    def get_tickerinfo(ticker: str):
        sql_cnx = get_sql_connection()
        sql_cursor = sql_cnx.cursor()
        ticker_encoded = get_string_base64_encoded(ticker)
        sql_cursor.execute("SELECT * FROM `ticker` WHERE `ticker`.`id` = %s", [ticker_encoded])
        ticker_row = sql_cursor.fetchone()
        ticker_columns = [column[0] for column in sql_cursor.description]
        sql_cnx.commit()
        sql_cursor.close()
        sql_cnx.close()
        responseData = {}
        if ticker_row is not None:
            responseData["status"] = "ok"
            responseData["results"] = dict(zip(ticker_columns, ticker_row))
            responseData["results"]["branding"] = {
                "logo_url": responseData["results"]["logo_url"],
                "icon_url": responseData["results"]["icon_url"],
            }
            del responseData["results"]["logo_url"]
            del responseData["results"]["icon_url"]
            responseData["results"]["address"] = {
                "address1": responseData["results"]["address1"],
                "city": responseData["results"]["city"],
                "state": responseData["results"]["state"],
                "postal_code": responseData["results"]["postal_code"]
            }
            del responseData["results"]["address1"]
            del responseData["results"]["city"]
            del responseData["results"]["state"]
            del responseData["results"]["postal_code"]
        else:
            responseData["status"] = "error"
        return responseData

    @staticmethod
    def proxy_polygon_resource(url: str):
        requestData = {"apiKey": api_key}
        remoteResponse = requests.get(url, params=requestData, stream=True)
        responseHeaders = {}
        for key, value in remoteResponse.headers.items():
            if key.lower() in ["content-type"]:
                responseHeaders[key] = value
        return {
            "headers": responseHeaders,
            "data": remoteResponse.raw
        }
