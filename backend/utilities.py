#!/usr/bin/env python3

import json, requests

@staticmethod
def call_api(endpoint, data):
    try:
        response = requests.post(endpoint, data=data, headers={"Referer": "https://cse437s.yufeim.com/api"})
    except Exception as ex:
        raise RuntimeError(json.dumps(ex))
    result = response.json()
    print(result)
    if "error" in result:
        raise PermissionError(json.dumps(result))
    return response.json()
