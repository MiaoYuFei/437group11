from typing import Union, Dict
import pandas as pd
import requests
import asyncio
import aiohttp
import datetime
from functools import lru_cache
import concurrent.futures
import sys
import os
import inspect

parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
sys.path.append(parent_dir)
import api_keys


# helper functions
def int_check(num_input: int, cap=50000):
    if type(num_input) == int:
        if num_input < 1:
            print("ERROR: arg timeintervalscale can not be less than 1")
            return None
        if num_input > cap:
            print("Attension: input>max value cap, auto scale input to cap")
            num_input = cap
        return num_input
    elif type(num_input) == float:
        if num_input.is_integer() == True:
            num_input = int(num_input)
            if num_input < 1:
                print("ERROR: arg timeintervalscale can not be less than 1")
                return None
            if num_input > cap:
                print("Attension: input>max value cap, auto scale input to cap")
                num_input = cap
            return num_input
        else:
            print("ERROR: arg timeintervalscale, not an int but a float")
            return None
    else:
        print("ERROR: arg timeintervalscale, not an int")
        return None


def pointer(df: pd.DataFrame, i: int, col: str):
    """
    :param df: dataframe
    :param i: row number
    :param col: col name in str
    :return: pointed cell.
    """
    return df.iloc[i, df.columns.get_loc(col)]


def read_xlsx(file_name):
    """
    require openpyxl and concurrent.futures
    :param file_name: xlsx file name
    :return: a dict of dataframes
    """

    def read_sheet(sheet_name, file_name):
        df = pd.read_excel(file_name, sheet_name=sheet_name)
        return sheet_name, df

    df_dict = {}
    with pd.ExcelFile(file_name) as xlsx:
        sheet_names = xlsx.sheet_names
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(read_sheet, sheet_name, file_name) for sheet_name in sheet_names]

            for result in concurrent.futures.as_completed(results):
                sheet_name, df = result.result()
                df_dict[sheet_name] = df
    return df_dict


@lru_cache()
def unix_time_to_datetime(unix_int: int) -> datetime.datetime:
    """
    :param unix_int: int of unix time
    :return: datetime in UTC
    """
    return datetime.datetime.utcfromtimestamp(unix_int / 1000.0)


async def get_data_from_urls(urls_dict: Dict[str, str]) -> Dict[str, pd.DataFrame]:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for ticker, url in urls_dict.items():
            task = asyncio.create_task(get_data_from_url(ticker, url, session))
            tasks.append(task)
        results = await asyncio.gather(*tasks)

        data_dict = {}
        for ticker, result in zip(urls_dict.keys(), results):
            data_dict[ticker] = result

        return data_dict


async def get_data_from_url(ticker: str, url: str, session) -> pd.DataFrame:
    try:
        async with session.get(url=url) as response:
            j = await response.json()
            if isinstance(j, dict): # single day would return only a dict for each ticker, or ticker info
                if "results" in j.keys():
                    df = pd.json_normalize(j["results"])
                else:
                    df = pd.DataFrame.from_dict(j, orient='index').T #singelday 
            elif isinstance(j["results"], list): # list of dicts for most cases
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
            return df
    except Exception as e:
        print("Unable to get ticker {} due to {}.".format(ticker, e.__class__))


def get_data_from_single_url(url: str) -> pd.DataFrame:
    j = requests.get(url).json()
    if isinstance(j["results"], list):
        df = pd.DataFrame(j["results"])
        while "next_url" in j.keys():
            next_url = j["next_url"] + "&apiKey=" + api_keys.poly_dict["api_key"]
            j = requests.get(next_url).json()
            df = pd.concat([df, pd.DataFrame.from_dict(j["results"])])
    else:
        df = pd.json_normalize(j["results"])
        while "next_url" in j.keys():
            next_url = j["next_url"] + "&apiKey=" + api_keys.poly_dict["api_key"]
            j = requests.get(next_url).json()
            df = pd.concat([df, pd.DataFrame.from_dict(j["results"])])
    return df


def get_method_info(cls) -> dict:
    """get all methods in a class, does not list subclass method"""
    methods = {}
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        signature = inspect.signature(method)
        args = []
        varargs = None
        kwargs = None
        defaults = []
        for param in signature.parameters.values():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                varargs = param.name
            elif param.kind == inspect.Parameter.VAR_KEYWORD:
                kwargs = param.name
            else:
                args.append(param.name)
                if param.default != inspect.Parameter.empty:
                    defaults.append(param.default)
        methods[name] = {
            'args': args,
            'varargs': varargs,
            'kwargs': kwargs,
            'defaults': defaults
        }
    return methods


def url_difference(url1: str, url2: str) -> str:
    """
    Returns the difference between two urls as a string
    """
    url1_parts = url1.split("/")
    url2_parts = url2.split("/")
    min_len = min(len(url1_parts), len(url2_parts))
    for i in range(min_len):
        if url1_parts[i] != url2_parts[i]:
            return "/".join(url1_parts[i:])
    return ""
