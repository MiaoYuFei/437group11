#!/usr/bin/env python3

import os

from utilities import call_api_get

script_path = os.path.realpath(os.path.dirname(__file__))

api_key = "GNthmWT9qYGm57QwnIJ_orim_uN5mbc0"

class newsdata_helper:
    def get_news_by_ticker(self, ticker: str):
        endpoint = "https://api.polygon.io/v2/reference/news"
        requestData = {"apiKey": api_key, "ticker": ticker, "sort": "published_utc", "order": "desc"}
        return call_api_get(endpoint, requestData)
