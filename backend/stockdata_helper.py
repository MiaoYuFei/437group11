#!/usr/bin/env python3

import os

import requests
from utilities import call_api_get

script_path = os.path.realpath(os.path.dirname(__file__))

api_key = "GNthmWT9qYGm57QwnIJ_orim_uN5mbc0"

class stockdata_helper:

    def get_aggregates(self, ticker: str, start_date: str, end_date: str):
        endpoint = "https://api.polygon.io/v2/aggs/ticker/{0}/range/1/hour/{1}/{2}".format(ticker, start_date, end_date)
        requestData = {"apiKey": api_key, "adjusted": "true", "sort": "desc", "limit": "1000"}
        return call_api_get(endpoint, requestData)

    def get_tickerinfo(self, ticker: str):
        endpoint = "https://api.polygon.io/v3/reference/tickers/{}".format(ticker)
        requestData = {"apiKey": api_key}
        return call_api_get(endpoint, requestData)

    def proxy_polygon_resource(self, url: str):
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
