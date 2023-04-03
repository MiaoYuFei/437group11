#!/usr/bin/env python3

import time
import firebase_helper
from utilities import get_sql_connection

class newsdata_firebase_bridge:

    @staticmethod
    def set_user_news_like_firebase(news_id: str, user_id: str, liked: bool):
        sql_cnx = get_sql_connection()
        sql_cursor = sql_cnx.cursor()
        sql_query = \
            "SELECT t.`ticker` \
            FROM `news_tickers` nt \
            INNER JOIN `ticker` t ON t.`id` = nt.`ticker_id` \
            WHERE nt.`news_id` = %s;"
        sql_cursor.execute(sql_query, [news_id])
        data_rows = sql_cursor.fetchall()
        sql_cursor.close()
        sql_cnx.close()
        data_list = [x[0] for x in data_rows]
        milliseconds1 = int(round(time.time() * 1000))
        doc_ticker_hash = firebase_helper.get_db().collection("tickers").document("ticker_hash").get()
        doc_ref_user_ticker_pref = firebase_helper.get_db().collection("user_ticker_pref").document(user_id)
        for ticker in data_list:
            ticker_hash = doc_ticker_hash.get(ticker)
            if ticker_hash is None:
                continue
            doc_user_ticker_pref_dict = doc_ref_user_ticker_pref.get().to_dict()
            if ticker_hash in doc_user_ticker_pref_dict:
                if liked == True:
                    doc_user_ticker_pref_dict[ticker_hash] += 1
                else:
                    doc_user_ticker_pref_dict[ticker_hash] -= 1
            doc_ref_user_ticker_pref.update(doc_user_ticker_pref_dict)
        milliseconds2 = int(round(time.time() * 1000))
        print("time: " + str(milliseconds2 - milliseconds1) + "ms")

    @staticmethod
    def get_user_news_recommendation_firebase(user_id: str, offset: int = 0) -> dict:
        print("get_user_news_recommendation_firebase")

        return {
            "newsIdList": [],
            "totalCount": 0
        }
