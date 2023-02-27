import sys
import os
sys.path.insert(1, 'data_poly/')
import poly_url
import poly_helper
import poly_getdata
import api_keys as api

ticker = "AAPL"

api_keys = api.poly_dict["api_key"]
url_factory = poly_url.PolyUrlFactory(api_keys)
url = url_factory.ReferenceData.news(url_factory, ticker)
df = poly_helper.get_data_from_single_url(url)