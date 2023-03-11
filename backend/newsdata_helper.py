#!/usr/bin/env python3

import os, json
from utilities import call_api_polygon

script_path = os.path.realpath(os.path.dirname(__file__))

api_key = "UlZ5J8DytULKSiAyj92pWLJrQVpehxkH"

class newsdata_helper:

    def get_aggregates(self, ticker: str, start_date: str, end_date: str):
        endpoint = "https://api.polygon.io/v2/aggs/ticker/{0}/range/1/hour/{1}/{2}?adjusted=true&sort=desc&limit=1000&apiKey={3}".format(ticker, start_date, end_date, api_key)
        data = {ticker: ticker, start_date: start_date, end_date: end_date}
        response = call_api_polygon(endpoint, data)
        return response
