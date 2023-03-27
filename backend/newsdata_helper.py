#!/usr/bin/env python3

import os

from utilities import get_string_base64_encoded, get_sql_connection

script_path = os.path.realpath(os.path.dirname(__file__))

api_key = "GNthmWT9qYGm57QwnIJ_orim_uN5mbc0"

class newsdata_helper:

    @staticmethod
    def get_news_latest(offset: int = 0):
        sql_cnx = get_sql_connection()
        sql_cursor = sql_cnx.cursor()
        if offset == 0:
            sql_query = \
                "SELECT COUNT(DISTINCT n.`id`) as total_rows \
                FROM `news` n \
                INNER JOIN `news_tickers` nt ON n.`id` = nt.`news_id` \
                INNER JOIN `ticker` t ON nt.`ticker_id` = t.`id`;"
            sql_cursor.execute(sql_query)
            news_total_count = sql_cursor.fetchone()[0]
        else:
            news_total_count = None
        sql_query = \
            "SELECT n.*, ( \
                SELECT GROUP_CONCAT(DISTINCT t.`category` SEPARATOR ',') \
                FROM `ticker` t \
                INNER JOIN `news_tickers` nt ON nt.`ticker_id` = t.`id` \
                WHERE nt.`news_id` = n.`id` \
                ) AS categories, ( \
                SELECT GROUP_CONCAT(DISTINCT t.`ticker` SEPARATOR ',') \
                FROM `ticker` t \
                INNER JOIN `news_tickers` nt ON nt.`ticker_id` = t.`id` \
                WHERE nt.`news_id` = n.`id` \
            ) AS tickers \
            FROM `news` n \
            INNER JOIN `news_tickers` nt ON n.`id` = nt.`news_id` \
            INNER JOIN `ticker` t ON nt.`ticker_id` = t.`id` \
            GROUP BY n.`id` \
            ORDER BY n.`article_datetime` DESC \
            LIMIT 10 OFFSET %s;"
        sql_cursor.execute(sql_query, [offset])
        news_rows = sql_cursor.fetchall()
        news_columns = [column[0] for column in sql_cursor.description]
        news_list = [dict(zip(news_columns, news_row)) for news_row in news_rows]
        for news in news_list:
            news["article"] = {
                "title": news["article_title"],
                "description": news["article_description"],
                "keywords": news["article_keywords"],
                "datetime": news["article_datetime"],
                "url": news["article_url"],
            }
            del news["article_title"]
            del news["article_description"]
            del news["article_keywords"]
            del news["article_datetime"]
            del news["article_url"]
            news["cover_image"] = {
                "url": news["cover_image_url"],
            }
            del news["cover_image_url"]
            news["publisher"] = {
                "name": news["publisher_name"],
                "homepage": {
                    "url": news["publisher_homepage_url"],
                },
                "logo": {
                    "url": news["publisher_logo_url"],
                },
            }
            del news["publisher_name"]
            del news["publisher_homepage_url"]
            del news["publisher_logo_url"]
            if news["tickers"] is not None:
                news["tickers"] = news["tickers"].split(",")
            else:
                news["tickers"] = []
            if news["categories"] is not None:
                news["categories"] = news["categories"].split(",")
            else:
                news["categories"] = []
        sql_cnx.commit()
        sql_cursor.close()
        sql_cnx.close()
        
        responseData = {}
        if news_rows is not None:
            responseData["status"] = "ok"
            if news_total_count is not None:
                responseData["total_count"] = news_total_count
            responseData["results"] = news_list
        else:
            responseData["status"] = "error"
        
        return responseData

    @staticmethod
    def get_news_by_ticker(ticker: str, offset: int = 0):
        sql_cnx = get_sql_connection()
        sql_cursor = sql_cnx.cursor()
        ticker_encoded = get_string_base64_encoded(ticker)
        if offset == 0:
            sql_query = "SELECT count(*) \
                FROM news n \
                INNER JOIN `news_tickers` nt ON n.id = nt.news_id \
                WHERE nt.ticker_id = %s;"
            sql_cursor.execute(sql_query, [ticker_encoded])
            news_total_count = sql_cursor.fetchone()[0]
        else:
            news_total_count = None
        sql_query = \
            "SELECT n.*, ( \
                SELECT GROUP_CONCAT(DISTINCT t.`category` SEPARATOR ',') \
                FROM `ticker` t \
                INNER JOIN `news_tickers` nt ON nt.`ticker_id` = t.`id` \
                WHERE nt.`news_id` = n.`id` \
                ) AS categories, ( \
                    SELECT GROUP_CONCAT(DISTINCT t.`ticker` SEPARATOR ',') \
                    FROM `ticker` t \
                    INNER JOIN `news_tickers` nt ON nt.`ticker_id` = t.`id` \
                    WHERE nt.`news_id` = n.`id` \
                ) AS tickers \
            FROM news n \
            INNER JOIN `news_tickers` nt ON n.`id` = nt.`news_id` \
            INNER JOIN `ticker` t ON nt.`ticker_id` = t.`id` \
            WHERE t.`id` = %s LIMIT 10 OFFSET %s;"
        sql_cursor.execute(sql_query, [ticker_encoded, offset])
        news_rows = sql_cursor.fetchall()
        news_columns = [column[0] for column in sql_cursor.description]
        news_list = [dict(zip(news_columns, news_row)) for news_row in news_rows]
        for news in news_list:
            news["article"] = {
                "title": news["article_title"],
                "description": news["article_description"],
                "keywords": news["article_keywords"],
                "datetime": news["article_datetime"],
                "url": news["article_url"],
            }
            del news["article_title"]
            del news["article_description"]
            del news["article_keywords"]
            del news["article_datetime"]
            del news["article_url"]
            news["cover_image"] = {
                "url": news["cover_image_url"],
            }
            del news["cover_image_url"]
            news["publisher"] = {
                "name": news["publisher_name"],
                "homepage": {
                    "url": news["publisher_homepage_url"],
                },
                "logo": {
                    "url": news["publisher_logo_url"],
                },
            }
            del news["publisher_name"]
            del news["publisher_homepage_url"]
            del news["publisher_logo_url"]
            if news["tickers"] is not None:
                news["tickers"] = news["tickers"].split(",")
                news["tickers"].insert(0, news["tickers"].pop(news["tickers"].index(ticker)))
            else:
                news["tickers"] = [ticker]
            if news["categories"] is not None:
                news["categories"] = news["categories"].split(",")
            else:
                news["categories"] = []
        sql_cnx.commit()
        sql_cursor.close()
        sql_cnx.close()

        responseData = {}
        if news_rows is not None:
            responseData["status"] = "ok"
            if news_total_count is not None:
                responseData["total_count"] = news_total_count
            responseData["results"] = news_list
        else:
            responseData["status"] = "error"
        
        return responseData

    @staticmethod
    def get_news_by_category(category: str, offset: int = 0):
        sql_cnx = get_sql_connection()
        sql_cursor = sql_cnx.cursor()
        if offset == 0:
            sql_query = \
            "SELECT COUNT(DISTINCT n.id) as total_rows \
            FROM `news` n \
            INNER JOIN `news_tickers` nt ON n.`id` = nt.`news_id` \
            INNER JOIN `ticker` t ON nt.`ticker_id` = t.`id` \
            WHERE t.`category` = %s"
            sql_cursor.execute(sql_query, [category])
            news_total_count = sql_cursor.fetchone()[0]
        else:
            news_total_count = None
        sql_query = \
            "SELECT n.*, ( \
                SELECT GROUP_CONCAT(DISTINCT t.`category` SEPARATOR ',') \
                FROM `ticker` t \
                INNER JOIN `news_tickers` nt ON nt.`ticker_id` = t.`id` \
                WHERE nt.`news_id` = n.`id` \
                ) AS categories, ( \
                SELECT GROUP_CONCAT(DISTINCT t.`ticker` SEPARATOR ',') \
                FROM `ticker` t \
                INNER JOIN `news_tickers` nt ON nt.`ticker_id` = t.`id` \
                WHERE nt.`news_id` = n.`id` \
            ) AS tickers \
            FROM `news` n \
            INNER JOIN `news_tickers` nt ON n.`id` = nt.`news_id` \
            INNER JOIN `ticker` t ON nt.`ticker_id` = t.`id` \
            WHERE t.`category` = %s \
            GROUP BY n.`id` \
            ORDER BY n.`article_datetime` DESC \
            LIMIT 10 OFFSET %s;"
        sql_cursor.execute(sql_query, [category, offset])
        news_rows = sql_cursor.fetchall()
        news_columns = [column[0] for column in sql_cursor.description]
        news_list = [dict(zip(news_columns, news_row)) for news_row in news_rows]
        for news in news_list:
            news["article"] = {
                "title": news["article_title"],
                "description": news["article_description"],
                "keywords": news["article_keywords"],
                "datetime": news["article_datetime"],
                "url": news["article_url"],
            }
            del news["article_title"]
            del news["article_description"]
            del news["article_keywords"]
            del news["article_datetime"]
            del news["article_url"]
            news["cover_image"] = {
                "url": news["cover_image_url"],
            }
            del news["cover_image_url"]
            news["publisher"] = {
                "name": news["publisher_name"],
                "homepage": {
                    "url": news["publisher_homepage_url"],
                },
                "logo": {
                    "url": news["publisher_logo_url"],
                },
            }
            del news["publisher_name"]
            del news["publisher_homepage_url"]
            del news["publisher_logo_url"]
            if news["tickers"] is not None:
                news["tickers"] = news["tickers"].split(",")
            else:
                news["tickers"] = []
            if news["categories"] is not None:
                news["categories"] = news["categories"].split(",")
                news["categories"].insert(0, news["categories"].pop(news["categories"].index(category)))
            else:
                news["categories"] = []
        sql_cnx.commit()
        sql_cursor.close()
        sql_cnx.close()
        
        responseData = {}
        if news_rows is not None:
            responseData["status"] = "ok"
            if news_total_count is not None:
                responseData["total_count"] = news_total_count
            responseData["results"] = news_list
        else:
            responseData["status"] = "error"
        
        return responseData

    @staticmethod
    def search_news(q: str, offset: int = 0):
        sql_cnx = get_sql_connection()
        sql_cursor = sql_cnx.cursor()
        sql_search_query = "%" + q + "%"
        if offset == 0:
            sql_query = \
            "SELECT COUNT(DISTINCT(n.`id`)) as total_rows \
            FROM `news` n \
            INNER JOIN `news_tickers` nt ON n.`id` = nt.`news_id` \
            INNER JOIN `ticker` t ON nt.`ticker_id` = t.`id` \
            WHERE n.`article_title` LIKE %s OR n.`article_description` LIKE %s"
            sql_cursor.execute(sql_query, [sql_search_query, sql_search_query])
            news_total_count = sql_cursor.fetchone()[0]
        else:
            news_total_count = None
        sql_query = \
            "SELECT n.*, ( \
                SELECT GROUP_CONCAT(DISTINCT t.`category` SEPARATOR ',') \
                FROM `ticker` t \
                INNER JOIN `news_tickers` nt ON nt.`ticker_id` = t.`id` \
                WHERE nt.`news_id` = n.`id` \
                ) AS categories, ( \
                SELECT GROUP_CONCAT(DISTINCT t.`ticker` SEPARATOR ',') \
                FROM `ticker` t \
                INNER JOIN `news_tickers` nt ON nt.`ticker_id` = t.`id` \
                WHERE nt.`news_id` = n.`id` \
            ) AS tickers \
            FROM `news` n \
            INNER JOIN `news_tickers` nt ON n.`id` = nt.`news_id` \
            INNER JOIN `ticker` t ON nt.`ticker_id` = t.`id` \
            WHERE n.`article_title` LIKE %s OR n.`article_description` LIKE %s \
            GROUP BY n.`id` \
            ORDER BY n.`article_datetime` DESC \
            LIMIT 10 OFFSET %s;"
        sql_cursor.execute(sql_query, [sql_search_query, sql_search_query, offset])
        news_rows = sql_cursor.fetchall()
        news_columns = [column[0] for column in sql_cursor.description]
        news_list = [dict(zip(news_columns, news_row)) for news_row in news_rows]
        for news in news_list:
            news["article"] = {
                "title": news["article_title"],
                "description": news["article_description"],
                "keywords": news["article_keywords"],
                "datetime": news["article_datetime"],
                "url": news["article_url"],
            }
            del news["article_title"]
            del news["article_description"]
            del news["article_keywords"]
            del news["article_datetime"]
            del news["article_url"]
            news["cover_image"] = {
                "url": news["cover_image_url"],
            }
            del news["cover_image_url"]
            news["publisher"] = {
                "name": news["publisher_name"],
                "homepage": {
                    "url": news["publisher_homepage_url"],
                },
                "logo": {
                    "url": news["publisher_logo_url"],
                },
            }
            del news["publisher_name"]
            del news["publisher_homepage_url"]
            del news["publisher_logo_url"]
            if news["tickers"] is not None:
                news["tickers"] = news["tickers"].split(",")
            else:
                news["tickers"] = []
            if news["categories"] is not None:
                news["categories"] = news["categories"].split(",")
            else:
                news["categories"] = []
        sql_cnx.commit()
        sql_cursor.close()
        sql_cnx.close()
        
        responseData = {}
        if news_rows is not None:
            responseData["status"] = "ok"
            if news_total_count is not None:
                responseData["total_count"] = news_total_count
            responseData["results"] = news_list
        else:
            responseData["status"] = "error"
        
        return responseData
