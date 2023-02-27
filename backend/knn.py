# import data_poly.poly_url as poly_url
# import data_poly.poly_helper as poly_helper
# import api_keys as api

# ticker = "AAPL"

# api_keys = api.poly_dict["api_key"]
# url_factory = poly_url.PolyUrlFactory(api_keys)
# url = url_factory.ReferenceData.news(url_factory, ticker)
# df = poly_helper.get_data_from_single_url(url)
import pandas as pd
df = pd.read_json("test.json")
# df.iloc[:5].to_json("test.json")

for i in range(3):
    row = df.iloc[i]
    item = {
        "article": {
            "title": row["title"],
            "description": row["description"],
            "keywords": row["keywords"],
            "datetime": row["published_utc"],
            "url": row["article_url"]
        },
        "cover_image": {
            "url": row["image_url"]
        },
        "publisher": {
            "name": row["publisher"]["name"],
            "homepage": {
                "url": row["publisher"]["homepage_url"],
            },
            "logo":  {
                "url": row["publisher"]["logo_url"],
            },
        },
        "tickers": row["tickers"]
    }
    print(item)
