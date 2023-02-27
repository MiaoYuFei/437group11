import asyncio
import sys
import os
from typing import List, Union, Literal
from collections import OrderedDict
from datetime import datetime as dt
import pandas as pd

poly_dir = os.path.abspath(os.path.join(os.getcwd(), 'data_poly'))
sys.path.append(poly_dir)

import poly_helper as poly_helper
import poly_url as poly_url


async def get_tickers_data(ticker_lc: List[str], url_factory: poly_url.StockUrlFactory,
                           data_type: Union[Literal['price', 'div', 'info']] = "price", start: str = "2000-01-01",
                           time_interval: Literal["minute", "hour", "day", "week", "month", "quarter", "year"] = "day",
                           end: str = dt.now().strftime("%Y-%m-%d")) -> List[List[Union[str, pd.DataFrame]]]:
    """
    :param url_factory: url factory to generate urls
    :param ticker_lc: list of tickers
    :param data_type: price, volume, or open_interest
    :param start: start date
    :param time_interval: miniute,hour,day,week,month,quarter,year
    :param end: end date
    :return: list of ticker and dataframe
    """
    urls_dict = {}
    if data_type == "price":
        urls_dict = {
            ticker: url_factory.MarketData.range(url_factory, ticker, start=start, end=end, time_interval=time_interval)
            for ticker in ticker_lc}
    elif data_type == "div":
        urls_dict = {ticker: url_factory.ReferenceData.stock_div(url_factory, ticker) for ticker in
                                 ticker_lc}
    elif data_type == "info":
        urls_dict = {ticker: url_factory.ReferenceData.ticker_info(url_factory, ticker, date=end) for ticker
                                 in ticker_lc}
    else:
        print("data_type not supported for this function, please use url_factory to generate urls")
    df_dict = await poly_helper.get_data_from_urls(urls_dict)
    return df_dict


async def get_tickers_info(ticker_lc: List[str], t0_thresh="2015/01/01", full_data=False) -> pd.DataFrame:
    """
    :param: t0_thresh, date threshold (if ticker listed after cut off date, do not get data for ticker)
    combine results from get_ticker_info as a mxn dataframe
    """
    t0_thresh = pd.to_datetime(t0_thresh)
    results = await get_tickers_data(ticker_lc, t0=t0_thresh, data_type="info")
    output_df = pd.concat(results.values(), axis=0, keys=results.keys())
    output_df["list_date"] = pd.to_datetime(output_df["list_date"])
    if full_data:
        return output_df
    else:
        output_df = output_df[["ticker", "market", "locale", "type", "active", "currency_name", "list_date"]]
        if ("currency_name" in output_df.columns) and ("active" in output_df.columns) and (
                "list_date" in output_df.columns):
            output_df = output_df[
                (output_df["currency_name"] == "usd") & (output_df["active"])]  # & (df["list_date"] < t0_thresh)
        return output_df


async def get_adj_tickers_price(ticker_lc: List[str], t0_thresh="2015/01/01") -> pd.DataFrame:
    """
    :param ticker_lc: list of tickers to try to get adj price
    :param t0_thresh: cut off date, if ticker listed after thresh, do not get data for ticker
    :return: dataframe of adjusted volume adjusted price
    """
    t0_thresh = pd.to_datetime(t0_thresh)
    # get data
    price_dict, div_dict = await asyncio.gather(
        get_tickers_data(ticker_lc, t0=t0_thresh, data_type="price"),
        get_tickers_data(ticker_lc, t0=t0_thresh, data_type="div")
    )
    price_dict = dict((k, v) for k, v in price_dict.items() if v is not None)
    div_dict = dict((k, v) for k, v in div_dict.items() if v is not None)
    # process the dataframes
    price_dict = OrderedDict(
        {ticker: df.set_index(df["t"].apply(lambda x: poly_helper.unix_time_to_datetime(x))).rename_axis("date")["vw"] for
         ticker, df in price_dict.items()})
    div_dict = OrderedDict({ticker: df.set_index(df["ex_dividend_date"].apply(pd.to_datetime)).loc[:, "cash_amount"] for
                            ticker, df in div_dict.items() if not df.empty})

    # adjust the price assume reinvest dividend
    def div_adj_apply(series, div):
        """
        :param series: stock raw price in pandas series
        :param div: dividend per stock index by ex-dividend date
        :return: pandas series of the adjusted price
        """
        series = series.fillna(method='ffill')
        div_df = pd.merge_asof(series, div, right_index=True, left_index=True, tolerance=pd.Timedelta('1d'))
        div_df = div_df[div_df.vw.first_valid_index():]
        div_df.dropna(subset=['vw'], inplace=True)
        div_df.cash_amount.fillna(0, inplace=True)
        # Use the where() function to only perform the division if the value in the vw column is not 0
        div_df["post_delta_ratio"] = div_df.cash_amount.where(div_df.vw != 0, 0) / div_df.vw.where(div_df.vw != 0, 1)
        div_df["final_ratio"] = 1
        div_df["final_ratio"] = (div_df["post_delta_ratio"] + 1).cumprod()
        return div_df.vw * div_df.final_ratio

    # apply adjustment on all tickers
    valid_tickers = {ticker: price_dict[ticker] for ticker in price_dict.keys() if
                     ticker in div_dict and all([(div_dict[ticker] is not None), (not div_dict[ticker].empty)])}
    for ticker, df in valid_tickers.items():
        price_dict[ticker] = div_adj_apply(df, div_dict[ticker])

    return pd.DataFrame(price_dict).fillna(method='ffill')


def get_all_tickers(url_factory: poly_url.StockUrlFactory, just_ticker: bool=True) -> Union[pd.DataFrame, List[str]]:
    """
    :return: list of all tickers on us equity market, can be dataframe or list
    """
    df = poly_helper.get_data_from_single_url(url_factory.ReferenceData.tickers())
    if just_ticker:
        return df["ticker"].tolist()
    return df


# options
def get_options(url_factory: poly_url.OptionUrlFactory, ticker: Union[str,None]=None, underlying_ticker: Union[str,None]=None,
                             contract_type: Union[None, Literal["call", "put"]] = None,
                             expiration_date: Union[str, None] = None, as_of: str = dt.today().strftime("%Y-%m-%d"),
                             strike_price: Union[float, None] = None, expired: Union[None, bool] = None,
                             sort_asc: bool = True, limit: int = 1000,
                             sort: Union[None, Literal[
                                 "ticker", "underlying_ticker", "expiration_date", "strike_price"]] = None) -> pd.DataFrame:
    """
    :param ticker: ticker symbol
    :param expiration_date: expiration date of the option
    :param option_type: option type, "call" or "put"
    :return: dataframe of options
    """
    url = url_factory.ReferenceData.option_contracts(ticker=ticker, underlying_ticker=underlying_ticker,
                             contract_type=contract_type,
                             expiration_date=expiration_date, as_of=as_of,
                             strike_price=strike_price, expired=strike_price,
                             sort_asc=sort_asc, limit=limit,
                             sort=sort)
    return poly_helper.get_data_from_single_url(url)
