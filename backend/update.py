#!/usr/bin/env python3

import base64
from datetime import datetime
import re
import schedule
import signal
import threading
from tqdm import tqdm
import time
import unicodedata
from urllib.parse import parse_qs, urlparse
from background_worker import background_worker
from utilities import call_api_get, get_sic_category_code_from_sic_code, get_sql_connection

api_key = "GvMNwf24VUyug10vZZvP0P7a5nh9fJt0"

utc_datetime_format = "%Y-%m-%dT%H:%M:%SZ"

worker_update_tickers_running = False
worker_update_news_running = False
bw_update_tickers = None
bw_update_news = None

@staticmethod
def clean_string(s):
    s = s.strip()
    s = unicodedata.normalize("NFKD", s)
    s = re.sub(r"[^\x00-\x7F]+", "", s)
    return s

@staticmethod
def transform_api_ticker_details_to_sql(ticker_details: dict) -> list:
    sql_values = []
    sql_values.append(base64.b64encode(ticker_details["ticker"].encode('utf-8')).decode('utf-8'))
    sql_values.append(ticker_details["ticker"])
    sql_values.append(1 if ticker_details["active"] else 0)

    sql_values += [ticker_details.get("address", {}).get(key, None) for key in ["address1", "city", "postal_code", "state"]] or [None]*4
    sql_values  += [ticker_details.get("branding", {}).get(key, None) for key in ["icon_url", "logo_url"]] or [None]*2
    for key in ["cik", "composite_figi", "currency_name", "description", "homepage_url", "list_date", "locale", "market", \
                "market_cap", "name", "phone_number", "primary_exchange", "round_lot", "share_class_figi", "share_class_shares_outstanding", \
                "sic_code", "sic_description", "ticker_root", "total_employees", "type", "weighted_shares_outstanding"]:
        sql_values.append(ticker_details[key] if key in ticker_details else None)
    sql_values.append(get_sic_category_code_from_sic_code(ticker_details["sic_code"]) if "sic_code" in ticker_details else None)
    return tuple(sql_values)

@staticmethod
def get_tickerinfo_and_save(ticker, sql_values_list):
    sql_values_list.append(transform_api_ticker_details_to_sql(get_tickerinfo_polygon(ticker)["results"]))

@staticmethod
def get_tickerinfo_polygon(ticker: str):
    endpoint = "https://api.polygon.io/v3/reference/tickers/{}".format(ticker)
    requestData = {"apiKey": api_key}
    return call_api_get(endpoint, requestData)

@staticmethod
def get_news_polygon(cursor: str | None = None, start_date: str | None = None, end_date: str | None = None):
    endpoint = "https://api.polygon.io/v2/reference/news"
    requestData = {"apiKey": api_key, "limit": 1000, "sort": "published_utc", "order": "desc"}
    if cursor is not None:
        requestData["cursor"] = cursor
    if start_date is not None:
        requestData["published_utc.gte"] = start_date
    if end_date is not None:
        requestData["published_utc.lte"] = end_date
    return call_api_get(endpoint, requestData)

@staticmethod
def get_tickers(cursor: str | None = None):
    endpoint = "https://api.polygon.io/v3/reference/tickers"
    requestData = {"apiKey": api_key, "active": "true", "limit": "1000"}
    if cursor is not None:
        requestData["cursor"] = cursor
    return call_api_get(endpoint, requestData)

def worker_update_tickers(stop_event):
    api_cursor = None
    last_page = False
    while not stop_event.is_set() and not last_page:
        api_result_tickers = get_tickers(api_cursor)
        if "results" not in api_result_tickers:
            print(api_result_tickers)
            raise Exception("Error getting tickers")
        
        if "next_url" not in api_result_tickers:
            last_page = True
        else:
            api_cursor = parse_qs(urlparse(api_result_tickers["next_url"]).query)["cursor"][0]
        
        sql_values_list = []
        sql_conn = get_sql_connection()
        sql_cursor = sql_conn.cursor()

        threads = []
        max_threads = 6

        tqdm_object = tqdm(api_result_tickers["results"])
        tmp_ticker_list = []
        for ticker_item in tqdm_object:
            ticker = ticker_item["ticker"]
            if ticker in tmp_ticker_list:
                continue
            tmp_ticker_list.append(ticker)
            tqdm_object.set_description("Processing ticker {}".format(ticker))
            sql_cursor.execute("SELECT count(*) FROM `ticker` WHERE `ticker`.`ticker` = %s", [ticker])
            is_new_ticker = sql_cursor.fetchone()[0] <= 0
            if is_new_ticker:
                t = threading.Thread(target=get_tickerinfo_and_save, args=(ticker, sql_values_list))
                threads.append(t)
                t.start()
                while threading.active_count() > max_threads:
                    time.sleep(0.1)
        for t in threads:
            t.join()
        print("Will add {} tickers.".format(len(sql_values_list)))

        sql_query = \
            "INSERT INTO `ticker` \
                (`id`, `ticker`, `active`, `address1`, `city`, `postal_code`, `state`, `icon_url`, `logo_url`, `cik`, \
                `composite_figi`, `currency_name`, `description`, `homepage_url`, `list_date`, \
                `locale`, `market`, `market_cap`, `name`, `phone_number`, `primary_exchange`, `round_lot`, \
                `share_class_figi`, `share_class_shares_outstanding`, `sic_code`, `sic_description`, \
                `ticker_root`, `total_employees`, `type`, `weighted_shares_outstanding`, `category`) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        sql_cursor.executemany(sql_query, sql_values_list)
        sql_conn.commit()
        sql_cursor.close()
        sql_conn.close()
        sql_values_list.clear()
    global worker_update_tickers_running
    worker_update_tickers_running = False

def worker_update_news(stop_event):
    sql_conn = get_sql_connection()
    sql_cursor = sql_conn.cursor()

    sql_query = \
        "DELETE FROM `news` n \
        WHERE n.`article_datetime` < DATE_SUB(NOW(), INTERVAL 3 MONTH)"
    sql_cursor.execute(sql_query)

    sql_query = \
        "SELECT n.`article_datetime` \
        FROM `news` n \
        ORDER BY n.`article_datetime` DESC \
        LIMIT 1"
    sql_cursor.execute(sql_query)
    last_article_datetime = sql_cursor.fetchone()[0]
    start_datetime_string = last_article_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_datetime_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    api_cursor = None
    last_page = False
    while not stop_event.is_set() and not last_page:
        api_result_news = get_news_polygon(api_cursor, start_datetime_string, end_datetime_string)
        if "results" not in api_result_news:
            print(api_result_news)
            raise Exception("Error getting news")
        
        if "next_url" not in api_result_news:
            last_page = True
        else:
            api_cursor = parse_qs(urlparse(api_result_news["next_url"]).query)["cursor"][0]

        sql_values_list = []
        sql_values_tickers_list = []
        tqdm_object = tqdm(api_result_news["results"])
        for news_item in tqdm_object:
            id = news_item["id"]
            tqdm_object.set_description("Processing news {}".format(news_item["title"]))
            sql_cursor.execute("SELECT count(*) FROM `news` WHERE `news`.`id` = %s", [id])
            is_new_news = sql_cursor.fetchone()[0] <= 0
            if not is_new_news:
                continue
            sql_values = [
                news_item["id"],
                None if "title" not in news_item else clean_string(news_item["title"]),
                None if "description" not in news_item else clean_string(news_item["description"]),
                None if "keywords" not in news_item else ",".join(news_item["keywords"]),
                datetime.strptime(news_item["published_utc"], utc_datetime_format).strftime("%Y-%m-%d %H:%M:%S"),
                news_item["article_url"],
                None if "image_url" not in news_item else news_item["image_url"],
                news_item["publisher"]["name"],
                None if "homepage_url" not in news_item["publisher"] else news_item["publisher"]["homepage_url"],
                None if "logo_url" not in news_item["publisher"] else news_item["publisher"]["logo_url"]
            ]
            sql_values_list.append(sql_values)
            tickers = set(news_item["tickers"])
            for ticker in tickers:
                sql_values_tickers = [
                    news_item["id"],
                    base64.b64encode(ticker.encode('utf-8')).decode('utf-8')
                ]
                sql_values_tickers_list.append(sql_values_tickers)
        print("Will add {} news.".format(len(sql_values_list)))

        sql_query = \
            "INSERT INTO `news` \
                (`id`, `article_title`, `article_description`, `article_keywords`, `article_datetime`, `article_url`, \
                    `cover_image_url`, `publisher_name`, `publisher_homepage_url`, `publisher_logo_url`) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        sql_cursor.executemany(sql_query, sql_values_list)
        sql_query = \
            "INSERT INTO `news_tickers` \
                (`news_id`, `ticker_id`) \
            VALUES (%s, %s)"
        sql_cursor.executemany(sql_query, sql_values_tickers_list)
        sql_values_list.clear()
    sql_conn.commit()
    sql_cursor.close()
    sql_conn.close()
    global worker_update_news_running
    worker_update_news_running = False

def run_worker_update_news():
    global worker_update_news_running
    if worker_update_news_running:
        return
    worker_update_news_running = True
    global bw_update_news
    if bw_update_news is not None:
        bw_update_news.stop()
    bw_update_news = background_worker([worker_update_news])
    bw_update_news.start()

def run_worker_update_tickers():
    global worker_update_tickers_running
    if worker_update_tickers_running:
        return
    worker_update_tickers_running = True
    global bw_update_tickers
    if bw_update_tickers is not None:
        bw_update_tickers.stop()
    bw_update_tickers = background_worker([worker_update_tickers])
    bw_update_tickers.start()

def cleanup(arg1, arg2):
    global bw_update_news
    if bw_update_news is not None:
        bw_update_news.stop()
    global bw_update_tickers
    if bw_update_tickers is not None:
        bw_update_tickers.stop()
    exit(0)

schedule.clear()
job_run_worker_update_news = schedule.every().day.do(run_worker_update_news)
job_run_worker_update_tickers = schedule.every().day.do(run_worker_update_tickers)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

while True:
    schedule.run_pending()
    time.sleep(600)
# run_worker_update_news()
# run_worker_update_tickers()
