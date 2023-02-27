# imports
import pandas_market_calendars as mcal
from collections import OrderedDict
import requests
import pandas as pd
import numpy as np
import re
from datetime import datetime as dt, timedelta
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pyarrow.feather as feather
import itertools
from scipy.special import comb
import asyncio
import aiohttp
import warnings
from tqdm import tqdm
import sys  # add parent path
import api_keys  # in repo packages

warnings.simplefilter(action='ignore', category=FutureWarning)
sys.path.append("/Users/zerg/Desktop/Repos/PeterZergQuant")
sys.path.append("/Users/zerg/Desktop/Repos/PeterZergQuant/data_poly")
from poly_cleandata import *

# set up, hard code
base_url_poly = "https://api.polygon.io/"
api_url_poly = "&apiKey=" + api_keys.poly_dict["api_key"]
field_dict_poly = {}
req_dict_poly = {}
field_value_dict_poly = {}
default_value_dict_poly = {}
function_dict = {}
dict_LC_poly = [field_dict_poly, req_dict_poly, field_value_dict_poly, default_value_dict_poly, function_dict]



# helper function

async def filter_ticker(ticker_lc):
    output_lc = []
    bench_df = await get_adj_tickers_price(["SPY"])
    ticker_data = await get_adj_tickers_price(ticker_lc)
    for ticker in ticker_lc:
        if ticker in ticker_data.columns:
            if check_liquidity(ticker_data[[ticker]], bench_df):
                output_lc.append(ticker)
    return output_lc


def check_liquidity(stock_df, bench_mark_df):
    for data_date in bench_mark_df.index:
        if data_date not in stock_df.index:
            return False
    return True


async def get_data_from_url(ticker, url, session):
    try:
        async with session.get(url=url) as response:
            j = await response.json()
            if isinstance(j["results"], list):
                df = pd.DataFrame(j["results"])
                while "next_url" in j.keys():
                    next_url = j["next_url"] + "&apiKey=" + api_keys.poly_dict["api_key"]
                    async with session.get(url=next_url) as response:
                        j = await response.json()
                        df = pd.concat([df, pd.DataFrame.from_dict(j["results"])])
            else:
                key_set = set(j["results"].keys())
                if {"address"} <= key_set:
                    j["results"].pop("address")
                mydict = j["results"]
                if {"currency_name"} <= j["results"].keys():
                    df = pd.DataFrame(mydict, index=[0])  # is 1 line from stock info api
                else:
                    print("error for the non-list j results")
            return [ticker, df]
    except Exception as e:
        print("Unable to get ticker {} due to {}.".format(ticker, e.__class__))


async def get_data_from_urls(urls_dict):
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(
            *[get_data_from_url(ticker, urls_dict[ticker], session) for ticker in urls_dict.keys()])
        return ret


def valid_check(ticker, ref):
    if ticker in ref:
        return True
    else:
        return False


def surface_plot(df):
    # acquire the cartesian coordinate matrices from the matrix
    # x is cols, y is rows
    z = np.asarray(df).T
    (x, y) = np.meshgrid(np.arange(z.shape[0]), np.arange(z.shape[1]))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x, y, z, cmap=cm.jet)
    fig.set_size_inches(18.5, 10.5)
    plt.figure(figsize=(20, 20), dpi=80)
    ax.set_xlabel('datetime')
    ax.set_ylabel('duration')
    ax.set_zlabel('par yield')
    plt.show()
    return x, y, z


# Url functions

def polygon_system_setup():
    global dict_LC_poly
    global field_dict_poly
    global req_dict_poly
    global field_value_dict_poly
    global default_value_dict_poly
    default_value_dict_poly["function"] = "price_hist_data"

    # market data
    # stock_hist_data
    function = "price_hist_data"
    function_dict[function] = url_market_agg_data
    field_LC = ["ticker", "t0", "tn",
                "timeintervalscale", "timeinterval", "price_adj", "sortAD", "limit"]
    field_dict_poly[function] = field_LC
    req_LC = [1, 1, 1, 0, 0, 0, 0, 0]
    for i in range(len(field_LC)):
        req_dict_poly[(function, field_LC[i])] = req_LC[i]
    default_value_dict_poly[function, "timeinterval"] = "day"
    default_value_dict_poly[function, "timeintervalscale"] = 1
    default_value_dict_poly[function, "price_adj"] = True
    default_value_dict_poly[function, "sortAD"] = True
    default_value_dict_poly[function, "limit"] = 50000
    field_value_dict_poly[function, "timeinterval"] = ["minute", "hour", "day", "week", "month", "quarter", "year"]
    # stock_hist_data_singelday
    function = "stock_hist_data_singelday"
    function_dict[function] = url_stock_market_singleday
    field_LC = ["ticker", "t0",
                "price_adj", ]
    field_dict_poly[function] = field_LC
    req_LC = [1, 1, 0]
    for i in range(len(field_LC)):
        req_dict_poly[(function, field_LC[i])] = req_LC[i]
    default_value_dict_poly[function, "price_adj"] = True
    # stock orderflow
    function = "stock_hist_data_orderflow"
    function_dict[function] = url_trade_orderflow
    field_LC = ["ticker",
                "timestamp", "sortAD", "limit", "sortTimestamp"]
    field_dict_poly[function] = field_LC
    req_LC = [1, 0, 0, 0, 0]
    for i in range(len(field_LC)):
        req_dict_poly[(function, field_LC[i])] = req_LC[i]
    default_value_dict_poly[function, "timestamp"] = True
    default_value_dict_poly[function, "sortAD"] = True
    default_value_dict_poly[function, "limit"] = 1000
    default_value_dict_poly[function, "sortTimestamp"] = True
    # stock_quote
    function = "stock_quote"
    function_dict[function] = url_stock_quote
    field_LC = ["ticker"]
    field_dict_poly[function] = field_LC
    req_LC = [1]
    for i in range(len(field_LC)):
        req_dict_poly[(function, field_LC[i])] = req_LC[i]
    default_value_dict_poly[function, "timestamp"] = None
    default_value_dict_poly[function, "sortAD"] = True
    default_value_dict_poly[function, "limit"] = 5000
    default_value_dict_poly[function, "sortTimestamp"] = True
    # stock_quote
    function = "stock_quote"
    function_dict[function] = url_stock_quote
    field_LC = ["ticker"]
    field_dict_poly[function] = field_LC
    req_LC = [1]
    for i in range(len(field_LC)):
        req_dict_poly[(function, field_LC[i])] = req_LC[i]
    # option_quote
    function = "option_quote"
    function_dict[function] = url_option_quote
    field_LC = ["ticker"]
    field_dict_poly[function] = field_LC
    req_LC = [1]
    for i in range(len(field_LC)):
        req_dict_poly[(function, field_LC[i])] = req_LC[i]

    # reference data
    # financials
    function = "stock_financial"
    function_dict[function] = url_financials
    field_LC = ["ticker",
                "timeframe_FS", "include_sourcesTF", "sortAD", "limit", "sortRF"]
    field_dict_poly[function] = field_LC
    req_LC = [1, 0, 0, 0, 0, 0]
    for i in range(len(field_LC)):
        req_dict_poly[(function, field_LC[i])] = req_LC[i]
    default_value_dict_poly[function, "timeframe_FS"] = "annual"
    default_value_dict_poly[function, "include_sourcesTF"] = True
    default_value_dict_poly[function, "limit"] = 100
    default_value_dict_poly[function, "sortRF"] = True
    field_value_dict_poly["timeframe_FS"] = ["annual", "quarterly", None]
    # asset tickers
    function = "tickers"
    function_dict[function] = url_tickers
    field_LC = ["asset_type", "market", "active", "sort", "order", "limit"]
    field_dict_poly[function] = field_LC
    req_LC = [0, 0, 0, 0, 0, 0]
    for i in range(len(field_LC)):
        req_dict_poly[(function, field_LC[i])] = req_LC[i]
    default_value_dict_poly[function, "asset_type"] = "CS"
    default_value_dict_poly[function, "market"] = "stocks"
    default_value_dict_poly[function, "active"] = True
    default_value_dict_poly[function, "sort"] = "ticker"
    default_value_dict_poly[function, "order"] = "asc"
    default_value_dict_poly[function, "limit"] = 1000
    # crypto_tickers
    function = "crypto_list"
    function_dict[function] = url_crypto_list
    field_LC = ["market", "date", "active", "sort", "order", "limit"]
    field_dict_poly[function] = field_LC
    req_LC = [0, 0, 0, 0, 0, 0]
    for i in range(len(field_LC)):
        req_dict_poly[(function, field_LC[i])] = req_LC[i]
    default_value_dict_poly[function, "market"] = "crypto"
    default_value_dict_poly[function, "date"] = "2017-01-01"
    default_value_dict_poly[function, "active"] = True
    default_value_dict_poly[function, "sort"] = "ticker"
    default_value_dict_poly[function, "order"] = "asc"
    default_value_dict_poly[function, "limit"] = 1000
    # option_tickers
    function = "target_option_tickers"
    function_dict[function] = url_option_tickers
    field_LC = ["underlying_ticker", "data_date", "expired", "order", "limit", "sort"]
    field_dict_poly[function] = field_LC
    req_LC = [1, 0, 0, 0, 0, 0]
    for i in range(len(field_LC)):
        req_dict_poly[(function, field_LC[i])] = req_LC[i]
    default_value_dict_poly[function, "underlying_ticker"] = "SPX"
    default_value_dict_poly[function, "data_date"] = dt.now().strftime("%Y-%m-%d")
    default_value_dict_poly[function, "expired"] = True
    default_value_dict_poly[function, "order"] = "asc"
    default_value_dict_poly[function, "limit"] = 1000
    default_value_dict_poly[function, "sort"] = "expiration_date"
    # ticker info
    function = "ticker_info"
    function_dict[function] = url_ticker_info
    field_LC = ["ticker"]
    field_dict_poly[function] = field_LC
    req_LC = [1]
    for i in range(len(field_LC)):
        req_dict_poly[(function, field_LC[i])] = req_LC[i]
    # stock dividends info
    function = "stock_dividends"
    function_dict[function] = url_stock_div
    field_LC = ["ticker", "order", "limit", "sort"]
    field_dict_poly[function] = field_LC
    req_LC = [1, 0, 0, 0]
    for i in range(len(field_LC)):
        req_dict_poly[(function, field_LC[i])] = req_LC[i]
    default_value_dict_poly[function, "order"] = "asc"
    default_value_dict_poly[function, "limit"] = 1000
    default_value_dict_poly[function, "sort"] = "ex_dividend_date"
    # news
    function = "news"
    function_dict[function] = url_news
    field_LC = ["ticker", "limit", "sort", "order"]
    field_dict_poly[function] = field_LC
    req_LC = [1, 0, 0, 0]
    for i in range(len(field_LC)):
        req_dict_poly[(function, field_LC[i])] = req_LC[i]
    default_value_dict_poly[function, "order"] = "asc"
    default_value_dict_poly[function, "limit"] = 1000
    default_value_dict_poly[function, "sort"] = "published_date"


# market data
def url_market_agg_data(ticker, t0, tn, timeintervalscale=1, timeinterval="day", price_adj=True, sortAD=True,
                        limit=50000):
    """
    :param ticker: stock ticker, str, no exchange attach
    :param timeintervalscale: scaling factor for timeinterval, int>0
    :param timeinterval: size of the time window: [miniute,hour,day,week,month,quarter,year]
    :param t0: starting date, YYYY-MM-DD
    :param tn: end date, YYYY-MM-DD
    :param price_adj: Bool, results adjusts for splits. default adjusted=true
    :param sortAD: Bool, sort the results by timestamp, true=ascend=old at top, false=descend=new at top
    :param limit: Limits the number of base aggregates queried. Max 50000, default 5000.
    :return: url in str
    """
    # hard code:
    version = "v2"
    data_path = "aggs"
    # checks
    # t0 & tn
    pattern = '[1|2][0|9][0-9][0-9]-[0|1][0-9]-[0123][0-9]'
    pattern_alt = '[1|2][0|9][0-9][0-9]/[0|1][0-9]/[0123][0-9]'
    # t0
    if re.match(pattern_alt, t0):
        t0 = t0.replace('/', '-', 2)
    if not (re.match(pattern, t0)):
        print("ERROR: t0 not matching format for poly, YYYY/MM/DD")
    # tn
    if re.match(pattern_alt, tn):
        tn = tn.replace('/', '-', 2)
    if not (re.match(pattern, tn)):
        print("ERROR: tn not matching format for poly, YYYY/MM/DD")
    # timeintervalscale
    if int_check(timeintervalscale) != None:
        timeintervalscale = int_check(timeintervalscale)
    else:
        print("timeintervalscale not int")
        return None
    # limit
    if int_check(limit) != None:
        limit = int_check(limit)
    else:
        print("timeinterval value not valid")
        return None
    # not going to check t0 and tn since data_poly checks it
    # function fields
    # adj
    if price_adj == True:
        price_adj = "true"
    else:
        price_adj = "false"
    # sort
    if sortAD == True:
        order = "asc"
    else:
        order = "desc"

    # url
    req_url = version + "/" + data_path + "/ticker/" + ticker + "/range/" + str(
        timeintervalscale) + "/" + timeinterval + "/" + t0 + "/" + tn
    optional_url = "?" + "adjusted=" + price_adj + "&sort=" + order + "&limit=" + str(limit)
    url = base_url_poly + req_url + optional_url + api_url_poly
    return url
    # January 1, 1970 is the starting time for "n", The Unix Msec timestamp


def url_stock_market_singleday(ticker, t0, price_adj=True):
    """
    :param ticker: stock ticker, str, no exchange
    :param t0: date, YYYY-MM-DD
    :param price_adj: Bool, results adjusts for splits. default adjusted=true
    :return: url in str
    """
    # hard code:
    version = "v1"
    data_path = "open-close"
    # function fields
    if price_adj:  # adj
        price_adj = "true"
    else:
        price_adj = "false"
    # url
    req_url = version + "/" + data_path + "/" + ticker + "/" + t0
    optional_url = "?" + "adjusted=" + price_adj
    url = base_url_poly + req_url + optional_url + api_url_poly
    return url


def url_trade_orderflow(ticker, timestamp=None, sortAD=True, limit=5000, sortTimestamp=True):
    """
    :param ticker: stock ticker, str, no exchange attach
    :param timestamp: e.g. "2022-04-08", YYYY-MM-DD, if None it would return the whole database
    :param sortAD: true=asc, false=desc
    :param limit: default 5000
    :param sortTimestamp: default true, sort by timestamp
    :return: url in str
    """
    # hard code:
    version = "v3"
    data_path = "trades"
    # function fields
    order = "asc" if sortAD == True else "desc"
    timestamp_sort = "timestamp" if sortTimestamp == True else None
    # url
    req_url = version + "/" + data_path + "/" + ticker
    optional_url = "?"
    if timestamp != None:
        optional_url += "timestamp=" + timestamp
    optional_url += "&order=" + order + "&limit=" + str(limit)
    if sortTimestamp != False:
        optional_url += "&sort=" + timestamp_sort
    url = base_url_poly + req_url + optional_url + api_url_poly
    return url


def url_stock_quote(ticker):
    version = "v2"
    data_path = "last"
    req_url = version + "/" + data_path + "/trade/" + ticker
    url = base_url_poly + req_url + "?apiKey=" + api_keys.poly_dict["api_key"]
    return url


def url_option_quote(ticker):
    version = "v3"
    data_path = "quotes"
    req_url = version + "/" + data_path + "/" + ticker
    url = base_url_poly + req_url + "?apiKey=" + api_keys.poly_dict["api_key"]
    return url


# ref data
def url_financials(ticker, timeframe_FS="annual", include_sourcesTF=True, sortAD=True, limit=100, sortRF=True):
    # hard code:
    version = "vX"
    data_path = "reference"
    req_url = version + "/" + data_path + "/" + "financials?ticker=" + ticker
    # options
    include_sources = "true" if include_sourcesTF == True else "false"
    order = "asc" if sortAD == True else "desc"
    sortRF_str = "period_of_report_date" if sortRF == True else "filing_date"
    limit_str = str(limit)
    # url optional
    optional_url = "&timeframe=" + timeframe_FS + "&include_sources=" + include_sources + "&order=" + order + "&limit=" + limit_str + "&sort=" + sortRF_str
    url = base_url_poly + req_url + optional_url + api_url_poly
    return url


def url_tickers(asset_type="CS", market="stocks", active="true", sort="ticker", order="asc", limit="1000"):
    """
    :return: url to generate tickers from polygon api
    """
    # hard code:
    version = "v3"
    data_path = "reference"
    req_url = version + "/" + data_path + "/" + "tickers?"
    # options
    optional_url = "type=" + asset_type + "&market=" + market + "&active=" + active + "&sort=" + sort + "&order=" + order + "&limit=" + limit
    url = base_url_poly + req_url + optional_url + api_url_poly
    return url


def url_crypto_list(market="crypto", date="2017-01-01", active=True, sort="ticker", order="asc", limit="1000"):
    """
    :param market: crypto market
    :param date: YYYY-MM-DD, currently does nothing, use data on 2017-01-01
    :param active:
    :param sort:
    :param order:
    :param limit: max 1000
    :return: df
    """
    version = "v3"
    data_path = "reference"
    req_url = version + "/" + data_path + "/tickers?" + "market=" + market
    active_str = "true" if active == True else "false"
    optional_url = "&date=" + date + "&active=" + active_str + "&sort=" + sort + "&order=" + order + "&limit=" + str(
        limit)
    url = base_url_poly + req_url + optional_url + api_url_poly
    return url


def url_option_tickers(underlying_ticker="SPX", data_date=dt.now().strftime("%Y-%m-%d"), expired=True,
                       order="asc", limit=1000, sort="expiration_date"):
    """
    :param underlying_ticker: ticker of underlying stock
    :param tn: cut off date, YYYY-MM-DD
    :param expired: if true, get historical option ticker
    :param limit: max 1000
    :return: url in str
    """
    version = "v3"
    data_path = "reference"
    req_url = version + "/" + data_path + "/" + "options/contracts?" + "underlying_ticker=" + underlying_ticker
    expired_str = "true" if expired else "false"
    optional_url = "&as_of=" + data_date + "&expired=" + expired_str + "&order=" + order + "&limit=" + str(
        limit) + "&sort=" + sort
    url = base_url_poly + req_url + optional_url + api_url_poly
    return url


def url_ticker_info(ticker):
    version = "v3"
    data_path = "reference"
    req_url = version + "/" + data_path + "/tickers/" + ticker
    url = base_url_poly + req_url + "?apiKey=" + api_keys.poly_dict["api_key"]
    return url


def url_stock_div(ticker, order="asc", limit="1000", sort="ex_dividend_date"):
    version = "v3"
    data_path = "reference"
    req_url = version + "/" + data_path + "/dividends?ticker=" + ticker
    optional_url = "&order=" + order + "&limit=" + limit + "&sort=" + sort
    url = base_url_poly + req_url + optional_url + api_url_poly
    return url


def url_news(ticker, order="asc", limit=1000, sort="published_utc"):
    version = "v2"
    data_path = "reference"
    req_url = version + "/" + data_path + "/news?ticker=" + ticker
    optional_url = "&order=" + order + "&limit=" + str(limit) + "&sort=" + sort
    url = base_url_poly + req_url + optional_url + api_url_poly
    return url


# action
def get_url(input_dict):
    def url_gen_wrapper_poly(func, args_LC):
        """
        :param func: function
        :param args_LC: list of arg inputs
        :return: string of url
        """
        return func(*args_LC)

    # check if function in dict, else set to default
    if "function" in input_dict:
        function = input_dict["function"]
    else:
        print("using default func")
        function = default_value_dict_poly["function"]
    # get url
    ref_arg_LC = field_dict_poly[function]
    args_LC = []  # lc of args to pass into the url generation functions
    for input_arg in ref_arg_LC:
        if req_dict_poly[(function, input_arg)] == 1:
            if input_arg in input_dict:
                args_LC.append(input_dict[input_arg])
            else:
                print("ERROR: Missing function arg: " + input_arg)
                return None
        else:
            if input_arg in input_dict:
                args_LC.append(input_dict[input_arg])
            else:
                args_LC.append(default_value_dict_poly[function, input_arg])
    func = function_dict[function]
    url = url_gen_wrapper_poly(func, args_LC)
    return url


def url_2_df(url):
    r = requests.get(url)
    j = r.json()
    if j['status'] != "OK":
        print("status: " + j['status'])
        return None
    df = pd.DataFrame(j['results'])
    while "next_url" in j.keys():
        next_url = j["next_url"] + api_url_poly
        r = requests.get(next_url)
        j = r.json()
        df_temp = pd.DataFrame.from_dict(j["results"])
        df = pd.concat([df, df_temp])
    return df


def url_2_dict(url):
    r = requests.get(url)
    j = r.json()
    if j['status'] != "OK":
        print("status: " + j['status'])
        return None
    return j['results']


def get_ticker_data(ticker, t0="2000-01-01", tn=dt.now().strftime("%Y-%m-%d"), crypto_target=False):
    if not isinstance(t0, str):
        t0 = t0.strftime("%Y-%m-%d")
    input_dict = {"ticker": ticker, 'function': "price_hist_data", 't0': t0, 'tn': tn}
    df = get_df_poly(input_dict)
    df["date"] = df["t"].apply(lambda x: unix_time_to_datetime(x))
    df = df.set_index(df["date"]).drop("date", axis=1)

    if not crypto_target:
        last_index = df.index[-1]
        last_trading_date = \
            mcal.get_calendar('NYSE').schedule(start_date=(dt.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
                                               end_date=dt.now().strftime("%Y-%m-%d")).index[-1].strftime(
                "%Y-%m-%d")
        last_trading_date = pd.to_datetime(last_trading_date)
        while last_index != last_trading_date:
            if last_index == 0:  # check if new df is going to be empty
                break
            input_dict["t0"] = last_index.strftime("%Y-%m-%d")
            df_temp = get_df_poly(input_dict)
            if df_temp.index[-1] == last_index:  # check if data does not have last trading date data
                break
            else:
                last_index = df_temp.index[-1]
            df = pd.concat([df, df_temp])
    return df


async def get_tickers_data(ticker_lc, data_type="price", t0="2000-01-01", timeinterval="day", tn=dt.now().strftime("%Y-%m-%d")):
    """
    :param ticker_lc: list of tickers
    :param data_type: price, volume, or open_interest
    :param t0: start date
    :param time_interval: miniute,hour,day,week,month,quarter,year
    :param tn: end date
    :return: df
    """
    urls_dict = OrderedDict()
    # format inputs
    if not isinstance(t0, str):
        t0 = t0.strftime("%Y-%m-%d")
    if not isinstance(tn, str):
        tn = tn.strftime("%Y-%m-%d")

    if data_type == "price":
        for ticker in ticker_lc:
            urls_dict[ticker] = url_market_agg_data(ticker, t0, tn, timeinterval=timeinterval)
    elif data_type == "div":
        for ticker in ticker_lc:
            urls_dict[ticker] = url_stock_div(ticker)
    elif data_type == "info":
        for ticker in ticker_lc:
            urls_dict[ticker] = url_ticker_info(ticker)
    else:
        print("data_type error")
    df_lc = await get_data_from_urls(urls_dict)
    return df_lc


async def get_option_quotes(tickers_lc):
    urls_dict = OrderedDict()
    for ticker in tickers_lc:
        input_dict = {"function": "option_quote", "ticker": ticker}
        urls_dict[ticker] = get_url(input_dict)
    df_lc = await get_data_from_urls(urls_dict)
    for i in range(len(df_lc)):
        df = df_lc[i][1]
        df_lc[i][1] = df.sort_values(by="ask_price", ascending=False)
    return df_lc


def get_df_poly(input_dict):
    # check if function in dict, else set to default
    if "function" in input_dict:
        function = input_dict["function"]
    else:
        function = default_value_dict_poly["function"]
    # get url
    url = get_url(input_dict)
    next_url = None
    r = requests.get(url)
    j = r.json()
    # check status
    if j['status'] != "OK":
        print("status: " + j['status'])
        return None
    # extract
    if function == "price_hist_data":
        result = j['results']
        df = pd.DataFrame.from_dict(result)
    elif function == "stock_hist_data_singelday":
        df = pd.Series(j).to_frame().T.drop("status", axis=1).set_index("from")
    elif function == "stock_hist_data_orderflow":
        result = j['results']
        df = pd.DataFrame.from_dict(result)
    elif function == "stock_quote":
        result = j['results']
        df = pd.DataFrame.from_dict(result)

    while "next_url" in j.keys():
        print("next_url")
        next_url = j["next_url"] + "&apiKey=" + api_keys.poly_dict["api_key"]
        r = requests.get(next_url)
        j = r.json()
        try:
            df_temp = pd.DataFrame.from_dict(j["results"])
        except:
            print(j)
        df = pd.concat([df, df_temp])
    return df


def financials_clean():
    """
    NOT ACTIVE. THIS IS AS REPORTED, different from ticker to ticker, and from time to time. :(
    """
    ticker = "BG"
    url = url_financials(ticker, timeframe_FS="annual", include_sourcesTF=True, sortAD=True, limit=100, sortRF=True)
    r = requests.get(url)
    j = r.json()
    result_lc = j["results"]
    for i in range(len(result_lc)):
        ref_dict = {k: result_lc[i][k] for k in
                    ['start_date', 'end_date', 'filing_date', 'cik', 'company_name', 'fiscal_period', 'fiscal_year']}
        financials_dict = result_lc[i]['financials']
        comprehensive_income_dict = financials_dict['comprehensive_income']
        comprehensive_income_df = pd.DataFrame()
        for item in comprehensive_income_dict:
            comprehensive_income_df[item] = [comprehensive_income_dict[item]["value"]]
        income_statement_dict = financials_dict['income_statement']


def get_all_tickers(justTicker=True):
    """
    :return: list of all tickers
    """
    url = url_tickers()
    df = url_2_df(url)
    if justTicker:
        return df["ticker"].tolist()
    else:
        return df


def get_all_liquid_tickers_in_us():
    ticker_lc = get_all_tickers()
    output_lc = filter_ticker(ticker_lc)
    return output_lc


def save_tickers(output_lc):
    df = pd.DataFrame(output_lc)
    file_path = r"C:\Users\Peter Yan\Desktop\repo\peterzergquant\Data\all_liquid_ticker"
    feather.write_feather(df, file_path)
    print("file output done")


def calc_div_adj_ratio(series, div):
    """
    :param series: stock raw price in pandas series
    :param div: dividend per stock index by ex-dividend date
    :return: pandas series of the final_ratio as pct ratio of the stock price at that date.
    """
    div_lc = []
    for i in range(len(div.index)):
        t = div.index[i]
        last_price = series.iloc[series.index.get_loc(t, method='nearest')]
        pct_div = div.iloc[i] / last_price
        div_lc.append(OrderedDict([('post_delta_ratio', pct_div), ('ex_div_t', t)]))
    df = pd.DataFrame.from_dict(div_lc).set_index('ex_div_t')
    df["final_ratio"] = 0
    for j in range(df.shape[0]):
        if j == 0:
            df.iloc[j, df.columns.get_loc("final_ratio")] = 1 + pointer(df, j, "post_delta_ratio")
        else:
            df.iloc[j, df.columns.get_loc("final_ratio")] = pointer(df, j - 1, "final_ratio") * (
                    1 + pointer(df, j, "post_delta_ratio"))
    return df["final_ratio"]


def div_adj_apply(series, div):
    """
    :param series: stock raw price in pandas series
    :param div: dividend per stock index by ex-dividend date
    :return: pandas series of the adjusted price
    """
    # apply div, assume same day reinvestment
    series = series.fillna(method='ffill')
    div_df = pd.merge(series, div, how='outer', left_index=True, right_index=True)
    div_df = div_df[div_df.vw.first_valid_index():]
    div_df.dropna(subset=['vw'], inplace=True)
    div_df["post_delta_ratio"] = (div_df.cash_amount / div_df.vw).fillna(0)
    div_df["final_ratio"] = (1 + div_df.post_delta_ratio.shift(1)).fillna(1)
    # div_df = div_df[div_df.post_delta_ratio != 0]
    for i in range(div_df.shape[0]):
        div_df.iloc[i, div_df.columns.get_loc("final_ratio")] = pointer(div_df, i - 1, "final_ratio") * (
                1 + pointer(div_df, i, "post_delta_ratio"))
    return div_df.vw * div_df.final_ratio


async def get_tickers_info(ticker_lc, t0_thresh="2015/01/01", full_data=False):
    """
    :param: t0_thresh, date threshold (if ticker listed after cut off date, do not get data for ticker)
    combine results from get_ticker_info as a mxn dataframe
    """
    t0_thresh = pd.to_datetime(t0_thresh)
    results = await get_tickers_data(ticker_lc, t0=t0_thresh, data_type="info")
    df_lc = []
    index_lc = []
    for result in results:
        if result is not None:
            df_lc.append(result[1])
            index_lc.append(result[0])
    df = pd.concat(df_lc)
    df.index = index_lc
    df["list_date"] = pd.to_datetime(df["list_date"])
    if full_data:
        return df
    else:
        df = df[["ticker", "market", "locale", "type", "active", "currency_name", "list_date"]]
        if ("currency_name" in df.columns) and ("active" in df.columns) and ("list_date" in df.columns):
            df = df[(df["currency_name"] == "usd") & (df["active"]) & (df["list_date"] < t0_thresh)]
        return df


async def get_adj_tickers_price(ticker_lc, t0_thresh="2015/01/01"):
    """
    :param ticker_lc: list of tickers to try to get adj price
    :param t0_thresh: cut off date, if ticker listed after thresh, do not get data for ticker
    :return: dataframe of adjusted vw price
    """
    t0_thresh = pd.to_datetime(t0_thresh)
    # get ticker info
    # print("get ticker info")
    df = await get_tickers_info(ticker_lc, t0_thresh=t0_thresh)

    # set up loop before get data
    # print("filter tickers")
    lc = []
    min_date = pd.to_datetime(df["list_date"].max())
    if t0_thresh > min_date:
        min_date = t0_thresh
    for i in range(df.shape[0]):
        lc.append(OrderedDict([('ticker', df["ticker"].iloc[i]), ('t0', min_date)]))

    data_dic = OrderedDict()
    div_dic = OrderedDict()

    # get data
    # print("get stock & div data")
    # print("get stock data")
    df_lc = await get_tickers_data(ticker_lc, t0=t0_thresh, data_type="price")
    # print("get div data")
    div_lc = await get_tickers_data(ticker_lc, t0=t0_thresh, data_type="div")
    for ele in df_lc:
        ticker = ele[0]
        df = ele[1]
        if df.empty:
            pass
        else:
            df["date"] = df["t"].apply(lambda x: unix_time_to_datetime(x))
            df = df.set_index(df["date"]).drop("date", axis=1)
            data_dic[ticker] = df.loc[pd.to_datetime(df.index) > pd.to_datetime(min_date)]["vw"]
    for ele in div_lc:
        ticker = ele[0]
        df = ele[1]
        if df.empty:
            pass
        else:
            df["date"] = pd.to_datetime(df["ex_dividend_date"])
            df = df.set_index(df["date"]).drop("date", axis=1)
            div_dic[ticker] = df["cash_amount"]

    # apply div adj
    # print("apply adj price to stock data")
    for ticker in data_dic.keys():
        if ticker in div_dic:
            if all([(div_dic[ticker] is not None), (not div_dic[ticker].empty)]):
                data_dic[ticker] = div_adj_apply(data_dic[ticker], div_dic[ticker])
        # return with clean data
    df = pd.DataFrame(data_dic).fillna(method='ffill')
    na_dict = {}
    for col in df.columns:
        na_dict[col] = df[col].isna().sum()
    na_dict = {k: v for (k, v) in na_dict.items() if v < 10}
    df = df[list(na_dict.keys())]
    df = df[list(na_dict.keys())]
    return df


def select_ticker_liquidity(price_spread_thresh=0.05, cur_min_v_thresh=0, last_min_v_thresh=1, cur_min_flow_thresh=2000,
                            last_min_flow_thresh=4000):
    base_lc = get_all_tickers()
    # get data
    url = "https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers?apiKey=GNthmWT9qYGm57QwnIJ_orim_uN5mbc0"
    j = requests.get(url).json()
    selected_tickers_lc = []
    # market liquidity
    for ticker_dict in j['tickers']:
        ticker = ticker_dict["ticker"]
        if ticker not in base_lc:
            pass
        else:
            if ticker_dict["updated"] == 0:  # before market open
                last_v = ticker_dict["prevDay"]["v"]
                last_flow = last_v * ticker_dict["prevDay"]["vw"]
                if all([last_v > last_min_v_thresh, last_flow > last_min_flow_thresh]):
                    # pass liquidity check
                    selected_tickers_lc.append(ticker)
            else:
                price = ticker_dict["lastTrade"]["p"]
                ask = ticker_dict["lastQuote"]["P"]
                bid = ticker_dict["lastQuote"]["p"]

                current_v = ticker_dict["day"]["v"]
                last_v = ticker_dict["prevDay"]["v"]
                current_flow = current_v * ticker_dict["day"]["vw"]
                last_flow = last_v * ticker_dict["prevDay"]["vw"]
                if all([(ask - bid) / price < price_spread_thresh, current_v > cur_min_v_thresh,
                        last_v > last_min_v_thresh, current_flow > cur_min_flow_thresh,
                        last_flow > last_min_flow_thresh]):
                    # pass liquidity check
                    selected_tickers_lc.append(ticker)
    return selected_tickers_lc


async def eligible_stock(t0_thresh="2020-01-01"):
    selected_tickers_lc = select_ticker_liquidity()
    data_lc = await get_tickers_data(selected_tickers_lc, data_type="info")
    selected_tickers_lc = []
    for data in data_lc:
        ticker = data[0]
        info_df = data[1]
        if any(["type" not in info_df.columns]):
            pass
        elif all([info_df.active[0] == True, info_df.locale[0] == "us", info_df.type[0] == "CS",
                  info_df.currency_name[0] == "usd",
                  pd.to_datetime(data_lc[0][1].list_date[0]) < pd.to_datetime(t0_thresh)]):
            selected_tickers_lc.append(ticker)
    selected_tickers_lc = await filter_ticker(selected_tickers_lc)
    return selected_tickers_lc


async def get_tickers_news(ticker_lc):
    urls_dict = OrderedDict()
    for ticker in ticker_lc:
        urls_dict[ticker] = url_news(ticker)
    df_lc = await get_data_from_urls(urls_dict)
    return df_lc


# local data updates
def snapshot_us_equity(update_local=False, location="D:/data/raw"):
    url = "https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers?apiKey=GNthmWT9qYGm57QwnIJ_orim_uN5mbc0"
    df = pd.json_normalize(requests.get(url).json()["tickers"], sep='~')
    if update_local:
        feather.write_feather(df, location + "/local_snapshot_us_equity")
    return df


async def us_equity_info(tickers_lc=snapshot_us_equity().ticker.to_list(), update_local=False,
                         location="D:/data/raw"):
    df = await get_tickers_info(tickers_lc, full_data=True)
    if update_local:
        feather.write_feather(df, location + "/local_us_equity_info")
    return df


async def us_equity_news(tickers_lc=feather.read_feather(
    "D:/data/raw/local_snapshot_us_equity").ticker.to_list(), update_local=False,
                         location="D:/data/raw"):
    news_lc = await get_tickers_news(tickers_lc.ticker.to_list())
    news_df = pd.DataFrame()
    for data in news_lc:
        news_df = pd.concat([news_df, data[1]])
    if update_local:
        feather.write_feather(news_df, location + "/local_us_equity_news")
    return news_df


def knn_news(update_local=False, location="D:/data/raw"):
    df_snap = feather.read_feather("D:/data/raw/local_snapshot_us_equity")
    news_df = feather.read_feather("D:/data/raw/local_us_equity_news")

    ticker_arr = df_snap.ticker.to_numpy()
    knn_ticker = np.zeros(shape=(len(ticker_arr), len(ticker_arr)))
    ticker_maping = {k: v for v, k in enumerate(ticker_arr)}
    target_arr = news_df.tickers.to_numpy()
    ref = ticker_maping.keys()
    vec_valid_check = np.vectorize(valid_check)

    def df_modify(tuple_pair, df, ref_map):
        df[ref_map[tuple_pair[0]], ref_map[tuple_pair[1]]] += 1

    def combo_gen(x):
        def comb_index(n, k):
            count = comb(n, k, exact=True)
            index = np.fromiter(itertools.chain.from_iterable(itertools.combinations(range(n), k)),
                                int, count=count * k)
            return index.reshape(-1, k)

        # this is a lot faster than np.asarray(list(itertools.combinations(x, 2)))
        return x[comb_index(len(x), 2)]

    for x in tqdm(target_arr):
        checker = vec_valid_check(x, ref)  # check for invalid tickers
        del_index = np.asarray(np.where(checker == False))
        x = np.delete(x, del_index, axis=0)  # del these invalid tickers
        x_comb = combo_gen(x)
        for pair in x_comb:
            df_modify(pair, knn_ticker, ticker_maping)
    knn_df = pd.DataFrame(knn_ticker, columns=ticker_arr, index=ticker_arr)
    if update_local:
        feather.write_feather(knn_df, location+"/local_knn_news")
    return knn_df


async def local_update(up_snapshot_us_equity=True, up_us_equity_info=True):
    df_lc = []
    if up_snapshot_us_equity:
        df_snap = snapshot_us_equity(update_local=True)
        df_lc.append(df_snap)
    if up_us_equity_info:
        if up_snapshot_us_equity:
            df_info = await us_equity_info(tickers_lc=df_snap.ticker.to_list(), update_local=True)
        else:
            df_info = await us_equity_info(update_local=True)
        df_lc.append(df_info)
    return df_lc


# main
polygon_system_setup()
