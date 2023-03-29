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
                "SELECT COUNT(*) \
                FROM `news` n;"
            sql_cursor.execute(sql_query)
            news_total_count = sql_cursor.fetchone()[0]
        else:
            news_total_count = None
        sql_query = \
            "SELECT n.*, \
            GROUP_CONCAT(t.`ticker` SEPARATOR ',') AS tickers, \
            GROUP_CONCAT(DISTINCT t.`category` SEPARATOR ',') AS categories \
            FROM `news` n \
            LEFT JOIN `news_tickers` nt ON `n`.`id` = `nt`.`news_id` \
            INNER JOIN `ticker` t ON nt.`ticker_id` = `t`.`id` \
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
            sql_query = \
            "SELECT COUNT(*) \
            FROM `news_tickers` \
            WHERE `ticker_id` = %s;"
            sql_cursor.execute(sql_query, [ticker_encoded])
            news_total_count = sql_cursor.fetchone()[0]
        else:
            news_total_count = None
        sql_query = \
        "SELECT n.*, \
        GROUP_CONCAT(DISTINCT t2.`category` SEPARATOR ',') AS categories, \
        GROUP_CONCAT(t2.`ticker` SEPARATOR ',') AS tickers \
        FROM `ticker` t1 \
        INNER JOIN `news_tickers` nt1 ON nt1.`ticker_id` = t1.`id` \
        INNER JOIN `news` n ON n.`id` = nt1.`news_id` \
        INNER JOIN `news_tickers` nt2 ON nt2.`news_id` = n.`id` \
        INNER JOIN `ticker` t2 ON t2.`id` = nt2.`ticker_id` \
        WHERE t1.`id` = %s \
        GROUP BY n.`id` \
        LIMIT 10 OFFSET %s;"
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
            "SELECT COUNT(DISTINCT n.`id`) \
            FROM `ticker` t \
            INNER JOIN `news_tickers` nt ON nt.`ticker_id` = t.`id` \
            INNER JOIN `news` n ON n.`id` = nt.`news_id` \
            WHERE t.`category` = %s;"
            sql_cursor.execute(sql_query, [category])
            news_total_count = sql_cursor.fetchone()[0]
        else:
            news_total_count = None
        sql_query = \
        "SELECT n.*, \
        GROUP_CONCAT(DISTINCT t2.`category` SEPARATOR ',') AS categories, \
        GROUP_CONCAT(DISTINCT t2.`ticker` SEPARATOR ',') AS tickers \
        FROM `ticker` t1 \
        INNER JOIN `news_tickers` nt1 ON nt1.`ticker_id` = t1.`id` \
        INNER JOIN `news` n ON n.`id` = nt1.`news_id` \
        INNER JOIN `news_tickers` nt2 ON nt2.`news_id` = n.`id` \
        INNER JOIN `ticker` t2 ON t2.`id` = nt2.`ticker_id` \
        WHERE t1.`category` = %s \
        GROUP BY n.`id` \
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
            "SELECT COUNT(DISTINCT n.`id`) \
            FROM `news` n \
            INNER JOIN `news_tickers` nt ON n.`id` = nt.`news_id` \
            INNER JOIN `ticker` t ON nt.`ticker_id` = t.`id` \
            WHERE n.`article_title` LIKE %s OR n.`article_description` LIKE %s OR t.`ticker` = %s;"
            sql_cursor.execute(sql_query, [sql_search_query, sql_search_query, q])
            news_total_count = sql_cursor.fetchone()[0]
        else:
            news_total_count = None
        sql_query = \
            "SELECT n.*, \
            GROUP_CONCAT(DISTINCT t.`category` SEPARATOR ',') AS categories, \
			GROUP_CONCAT(DISTINCT t.`ticker` SEPARATOR ',') AS tickers \
            FROM `news` n \
            INNER JOIN `news_tickers` nt ON n.`id` = nt.`news_id` \
            INNER JOIN `ticker` t ON nt.`ticker_id` = t.`id` \
            WHERE n.`article_title` LIKE %s OR n.`article_description` LIKE %s OR t.`ticker` = %s \
            GROUP BY n.`id` \
            ORDER BY n.`article_datetime` DESC \
            LIMIT 10 OFFSET %s;"
        sql_cursor.execute(sql_query, [sql_search_query, sql_search_query, q, offset])
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
    def set_user_news_like(news_id: str, user_id: str, liked: bool):
        sql_cnx = get_sql_connection()
        sql_cursor = sql_cnx.cursor()
        sql_query = \
            "SELECT * \
            FROM `news_likecollect` \
            WHERE `news_id` = %s AND `user_id` = %s;"
        sql_cursor.execute(sql_query, [news_id, user_id])
        data_row = sql_cursor.fetchone()
        if data_row is None:
            sql_query = \
                "INSERT INTO `news_likecollect` (`news_id`, `user_id`, `liked`, `collected`) \
                VALUES (%s, %s, %s, %s);"
            sql_cursor.execute(sql_query, [news_id, user_id, 1 if liked else 0, 0])
        else:
            data_columns = [column[0] for column in sql_cursor.description]
            data_dict = dict(zip(data_columns, data_row))
            if liked == True:
                sql_query = \
                    "UPDATE `news_likecollect` \
                    SET `liked` = %s \
                    WHERE `id` = %s;"
                sql_cursor.execute(sql_query, [1, data_dict["id"]])
            else:
                if data_dict["collected"] == 0:
                    sql_query = \
                        "DELETE FROM `news_likecollect` \
                        WHERE `id` = %s;"
                    sql_cursor.execute(sql_query, [data_dict["id"]])
                else:
                    sql_query = \
                        "UPDATE `news_likecollect` \
                        SET `liked` = %s \
                        WHERE `id` = %s;"
                    sql_cursor.execute(sql_query, [0, data_dict["id"]])
        sql_cnx.commit()
        sql_cursor.close()
        sql_cnx.close()
        
        responseData = {}
        if data_row is not None:
            responseData["status"] = "ok"
        else:
            responseData["status"] = "error"
        
        return responseData

    @staticmethod
    def set_user_news_collect(news_id: str, user_id: str, collected: bool):
        sql_cnx = get_sql_connection()
        sql_cursor = sql_cnx.cursor()
        sql_query = \
            "SELECT * \
            FROM `news_likecollect` \
            WHERE `news_id` = %s AND `user_id` = %s;"
        sql_cursor.execute(sql_query, [news_id, user_id])
        data_row = sql_cursor.fetchone()
        if data_row is None:
            sql_query = \
                "INSERT INTO `news_likecollect` (`news_id`, `user_id`, `liked`, `collected`) \
                VALUES (%s, %s, %s, %s);"
            sql_cursor.execute(sql_query, [news_id, user_id, 0, 1 if collected else 0])
        else:
            data_columns = [column[0] for column in sql_cursor.description]
            data_dict = dict(zip(data_columns, data_row))
            if collected == True:
                sql_query = \
                    "UPDATE `news_likecollect` \
                    SET `collected` = %s \
                    WHERE `id` = %s;"
                sql_cursor.execute(sql_query, [1, data_dict["id"]])
            else:
                if data_dict["liked"] == 0:
                    sql_query = \
                        "DELETE FROM `news_likecollect` \
                        WHERE `id` = %s;"
                    sql_cursor.execute(sql_query, [data_dict["id"]])
                else:
                    sql_query = \
                        "UPDATE `news_likecollect` \
                        SET `collected` = %s \
                        WHERE `id` = %s;"
                    sql_cursor.execute(sql_query, [0, data_dict["id"]])
        sql_cnx.commit()
        sql_cursor.close()
        sql_cnx.close()
        
        responseData = {}
        if data_row is not None:
            responseData["status"] = "ok"
        else:
            responseData["status"] = "error"
        
        return responseData
