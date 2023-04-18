#!/usr/bin/env python3

import datetime
from newsdata_firebase_bridge import newsdata_firebase_bridge
from utilities import get_sql_connection, get_string_base64_encoded, process_news_response

import firebase_helper

api_key = "GvMNwf24VUyug10vZZvP0P7a5nh9fJt0"

class newsdata_helper:

    @staticmethod
    def get_news_latest(userId: str, offset: int = 0) -> dict:
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
        if userId == None:
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
        else:
            sql_query = \
                "SELECT n.*, \
                GROUP_CONCAT(t.`ticker` SEPARATOR ',') AS tickers, \
                GROUP_CONCAT(DISTINCT t.`category` SEPARATOR ',') AS categories, \
                MAX(nlc.`liked`) AS liked, \
                MAX(nlc.`collected`) AS collected \
                FROM `news` n \
                LEFT JOIN `news_tickers` nt ON `n`.`id` = `nt`.`news_id` \
                INNER JOIN `ticker` t ON nt.`ticker_id` = `t`.`id` \
                LEFT JOIN `news_likecollect` nlc ON nlc.`news_id` = n.`id` AND nlc.`user_id` = %s \
                GROUP BY n.`id` \
                ORDER BY n.`article_datetime` DESC \
                LIMIT 10 OFFSET %s;"
            sql_cursor.execute(sql_query, [userId, offset])
        news_rows = sql_cursor.fetchall()
        news_columns = [column[0] for column in sql_cursor.description]
        news_list = [dict(zip(news_columns, news_row)) for news_row in news_rows]
        sql_cursor.close()
        sql_cnx.close()
        process_news_response(news_list)
        responseData = {}
        responseData["newsList"] = news_list
        if news_total_count is not None:
            responseData["totalCount"] = news_total_count

        return responseData

    @staticmethod
    def get_news_by_ticker(ticker: str, userId: str, offset: int = 0) -> dict:
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
        if userId == None:
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
        else:
            sql_query = \
            "SELECT n.*, \
            GROUP_CONCAT(DISTINCT t2.`category` SEPARATOR ',') AS categories, \
            GROUP_CONCAT(t2.`ticker` SEPARATOR ',') AS tickers, \
            MAX(nlc.`liked`) AS liked, \
            MAX(nlc.`collected`) AS collected \
            FROM `ticker` t1 \
            INNER JOIN `news_tickers` nt1 ON nt1.`ticker_id` = t1.`id` \
            INNER JOIN `news` n ON n.`id` = nt1.`news_id` \
            INNER JOIN `news_tickers` nt2 ON nt2.`news_id` = n.`id` \
            INNER JOIN `ticker` t2 ON t2.`id` = nt2.`ticker_id` \
            LEFT JOIN `news_likecollect` nlc ON nlc.`news_id` = n.`id` AND nlc.`user_id` = %s \
            WHERE t1.`id` = %s \
            GROUP BY n.`id` \
            LIMIT 10 OFFSET %s;"
            sql_cursor.execute(sql_query, [userId, ticker_encoded, offset])
        news_rows = sql_cursor.fetchall()
        news_columns = [column[0] for column in sql_cursor.description]
        news_list = [dict(zip(news_columns, news_row)) for news_row in news_rows]
        sql_cursor.close()
        sql_cnx.close()
        process_news_response(news_list)
        responseData = {}
        responseData["newsList"] = news_list
        if news_total_count is not None:
            responseData["totalCount"] = news_total_count

        return responseData

    @staticmethod
    def get_news_by_category(category: str, userId: str, offset: int = 0) -> dict:
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
        if userId == None:
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
        else:
            sql_query = \
            "SELECT n.*, \
            GROUP_CONCAT(DISTINCT t2.`category` SEPARATOR ',') AS categories, \
            GROUP_CONCAT(DISTINCT t2.`ticker` SEPARATOR ',') AS tickers, \
            MAX(nlc.`liked`) AS liked, \
            MAX(nlc.`collected`) AS collected \
            FROM `ticker` t1 \
            INNER JOIN `news_tickers` nt1 ON nt1.`ticker_id` = t1.`id` \
            INNER JOIN `news` n ON n.`id` = nt1.`news_id` \
            INNER JOIN `news_tickers` nt2 ON nt2.`news_id` = n.`id` \
            INNER JOIN `ticker` t2 ON t2.`id` = nt2.`ticker_id` \
            LEFT JOIN `news_likecollect` nlc ON nlc.`news_id` = n.`id` AND nlc.`user_id` = %s \
            WHERE t1.`category` = %s \
            GROUP BY n.`id` \
            LIMIT 10 OFFSET %s;"
            sql_cursor.execute(sql_query, [userId, category, offset])
        news_rows = sql_cursor.fetchall()
        news_columns = [column[0] for column in sql_cursor.description]
        news_list = [dict(zip(news_columns, news_row)) for news_row in news_rows]
        sql_cursor.close()
        sql_cnx.close()
        process_news_response(news_list)
        responseData = {}
        responseData["newsList"] = news_list
        if news_total_count is not None:
            responseData["totalCount"] = news_total_count

        return responseData

    @staticmethod
    def search_news(q: str, userId: str, offset: int = 0) -> dict:
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
        if userId == None:
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
        else:
            sql_query = \
                "SELECT n.*, \
                GROUP_CONCAT(DISTINCT t.`category` SEPARATOR ',') AS categories, \
                GROUP_CONCAT(DISTINCT t.`ticker` SEPARATOR ',') AS tickers, \
                MAX(nlc.`liked`) AS liked, \
                MAX(nlc.`collected`) AS collected \
                FROM `news` n \
                INNER JOIN `news_tickers` nt ON n.`id` = nt.`news_id` \
                INNER JOIN `ticker` t ON nt.`ticker_id` = t.`id` \
                LEFT JOIN `news_likecollect` nlc ON nlc.`news_id` = n.`id` AND nlc.`user_id` = %s \
                WHERE n.`article_title` LIKE %s OR n.`article_description` LIKE %s OR t.`ticker` = %s \
                GROUP BY n.`id` \
                ORDER BY n.`article_datetime` DESC \
                LIMIT 10 OFFSET %s;"
            sql_cursor.execute(sql_query, [userId, sql_search_query, sql_search_query, q, offset])
        news_rows = sql_cursor.fetchall()
        news_columns = [column[0] for column in sql_cursor.description]
        news_list = [dict(zip(news_columns, news_row)) for news_row in news_rows]
        sql_cursor.close()
        sql_cnx.close()
        process_news_response(news_list)
        responseData = {}
        responseData["newsList"] = news_list
        if news_total_count is not None:
            responseData["totalCount"] = news_total_count

        return responseData

    @staticmethod
    def set_user_news_like(newsId: str, userId: str, liked: bool):
        sql_cnx = get_sql_connection()
        sql_cursor = sql_cnx.cursor()
        sql_query = \
            "SELECT * \
            FROM `news_likecollect` \
            WHERE `news_id` = %s AND `user_id` = %s;"
        sql_cursor.execute(sql_query, [newsId, userId])
        data_row = sql_cursor.fetchone()
        if data_row is None:
            sql_query = \
                "INSERT INTO `news_likecollect` (`news_id`, `user_id`, `liked`, `collected`) \
                VALUES (%s, %s, %s, %s);"
            sql_cursor.execute(sql_query, [newsId, userId, 1 if liked else 0, 0])
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
        newsdata_firebase_bridge.set_user_news_like_firebase(newsId, userId, liked)

    @staticmethod
    def set_user_news_collect(newsId: str, userId: str, collected: bool):
        sql_cnx = get_sql_connection()
        sql_cursor = sql_cnx.cursor()
        sql_query = \
            "SELECT * \
            FROM `news_likecollect` \
            WHERE `news_id` = %s AND `user_id` = %s;"
        sql_cursor.execute(sql_query, [newsId, userId])
        data_row = sql_cursor.fetchone()
        collect_datetime = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        if data_row is None:
            sql_query = \
                "INSERT INTO `news_likecollect` (`news_id`, `user_id`, `liked`, `collected`, `collect_datetime`) \
                VALUES (%s, %s, %s, %s, %s);"
            sql_cursor.execute(sql_query, [newsId, userId, 0, 1 if collected else 0, collect_datetime])
        else:
            data_columns = [column[0] for column in sql_cursor.description]
            data_dict = dict(zip(data_columns, data_row))
            if collected == True:
                sql_query = \
                    "UPDATE `news_likecollect` \
                    SET `collected` = %s, `collect_datetime` = %s \
                    WHERE `id` = %s;"
                sql_cursor.execute(sql_query, [1, collect_datetime, data_dict["id"]])
            else:
                if data_dict["liked"] == 0:
                    sql_query = \
                        "DELETE FROM `news_likecollect` \
                        WHERE `id` = %s;"
                    sql_cursor.execute(sql_query, [data_dict["id"]])
                else:
                    sql_query = \
                        "UPDATE `news_likecollect` \
                        SET `collected` = %s, `collect_datetime` = NULL \
                        WHERE `id` = %s;"
                    sql_cursor.execute(sql_query, [0, data_dict["id"]])
        sql_cnx.commit()
        sql_cursor.close()
        sql_cnx.close()

    @staticmethod
    def get_user_news_recommendation(userId: str, offset: int = 0) -> dict:
        if userId == None:
            raise PermissionError("User ID is required")
        preferences = firebase_helper.get_preferences(userId)
        if preferences is None:
            return None
        sql_cnx = get_sql_connection()
        sql_cursor = sql_cnx.cursor()

        category_list = [key for key, value in preferences.items() if value is True]
        category_count = len(category_list)
        if category_count == 0:
            return None
    
        if offset == 0:
            sql_query = \
                "SELECT COUNT(DISTINCT n.`id`) \
                FROM `ticker` t \
                INNER JOIN `news_tickers` nt ON nt.`ticker_id` = t.`id` \
                INNER JOIN `news` n ON n.id = nt.`news_id`"
            for i in range(category_count):
                if i == 0:
                    sql_query += " WHERE "
                sql_query += "t.`category` = %s"
                if i != category_count - 1:
                    sql_query += " OR "
            sql_cursor.execute(sql_query, category_list)
            data_total_count = sql_cursor.fetchone()[0]
        else:
            data_total_count = None
        sql_query = \
            "SELECT n.*, \
            GROUP_CONCAT(t.`ticker` SEPARATOR ',') AS tickers, \
            GROUP_CONCAT(DISTINCT t.`category` SEPARATOR ',') AS categories, \
            MAX(nlc.`liked`) AS liked, \
            MAX(nlc.`collected`) AS collected \
            FROM `news` n \
            LEFT JOIN `news_tickers` nt ON nt.`news_id` = n.`id` \
            LEFT JOIN `ticker` t ON nt.`ticker_id` = t.`id` \
            LEFT JOIN `news_likecollect` nlc ON nlc.`news_id` = n.`id` AND nlc.`user_id` = %s \
            WHERE n.`id` IN ( \
                SELECT nt.`news_id` \
                FROM `ticker` t \
                INNER JOIN `news_tickers` nt ON nt.`ticker_id` = t.`id`"
        for i in range(category_count):
            if i == 0:
                sql_query += " WHERE "
            sql_query += "t.`category` = %s "
            if i != category_count - 1:
                sql_query += "OR "
        sql_query += \
            ") \
            GROUP BY n.`id` \
            ORDER BY n.`article_datetime` DESC \
            LIMIT 10 OFFSET %s"
        sql_cursor.execute(sql_query, [userId] + category_list + [offset])
        data_rows = sql_cursor.fetchall()
        data_columns = [i[0] for i in sql_cursor.description]
        if data_total_count != 0:
            news_list = [dict(zip(data_columns, news_row)) for news_row in data_rows]
            process_news_response(news_list)
        else:
            news_list = []
        sql_cnx.commit()
        sql_cursor.close()
        sql_cnx.close()
        responseData = {}
        responseData["newsList"] = news_list
        if data_total_count is not None:
            responseData["totalCount"] = data_total_count

        return responseData

    @staticmethod
    def get_user_news_collection(user_id: str, offset: int = 0) -> dict:
        sql_cnx = get_sql_connection()
        sql_cursor = sql_cnx.cursor()
        if offset == 0:
            sql_query = \
            "SELECT COUNT(DISTINCT n.`id`) \
            FROM `news_likecollect` nlc \
            INNER JOIN `news` n ON n.`id` = nlc.`news_id` \
            WHERE nlc.`user_id` = %s AND nlc.`collected` = 1;"
            sql_cursor.execute(sql_query, [user_id])
            data_total_count = sql_cursor.fetchone()[0]
        else:
            data_total_count = None
        if data_total_count != 0:
            sql_query = \
                "SELECT n.*, \
                GROUP_CONCAT(DISTINCT t.`category` SEPARATOR ',') AS categories, \
                GROUP_CONCAT(DISTINCT t.`ticker` SEPARATOR ',') AS tickers, \
                MAX(nlc.`liked`) AS liked, \
                MAX(nlc.`collected`) AS collected, \
                MAX(nlc.`collect_datetime`) AS collect_datetime \
                FROM `news_likecollect` nlc \
                INNER JOIN `news` n ON n.`id` = nlc.`news_id` \
                INNER JOIN `news_tickers` nt ON nt.`news_id` = n.`id` \
                INNER JOIN `ticker` t ON t.`id` = nt.`ticker_id` \
                WHERE nlc.`user_id` = %s AND nlc.`collected` = 1 \
                GROUP BY n.`id` \
                ORDER BY collect_datetime DESC \
                LIMIT 10 OFFSET %s;"
            sql_cursor.execute(sql_query, [user_id, offset])
            data_rows = sql_cursor.fetchall()
            data_columns = [column[0] for column in sql_cursor.description]
        sql_cursor.close()
        sql_cnx.close()

        if data_total_count != 0:
            news_list = [dict(zip(data_columns, news_row)) for news_row in data_rows]
            process_news_response(news_list)
        else:
            news_list = []
        responseData = {}
        responseData["newsList"] = news_list
        if data_total_count is not None:
            responseData["totalCount"] = data_total_count

        return responseData
