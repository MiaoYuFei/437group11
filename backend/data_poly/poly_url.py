import sys
import os
from datetime import datetime as dt
from typing import Optional, Union, Literal
import urllib

# add poly directory to sys.path
poly_dir = os.path.abspath(os.path.join(os.getcwd(), 'data_poly'))
sys.path.append(poly_dir)


class PolyUrlFactory:
    BASE_URL = "https://api.polygon.io/"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "apiKey=" + self.api_key

    class MarketData:
        @staticmethod
        def range(self, ticker: str, start: str = "2000-01-01", end: str = dt.now().strftime("%Y-%m-%d"),
                  time_scale: int = 1, time_interval: Literal["minute","hour","day","week","month","quarter","year"]="day", price_adj: bool = True, sort_asc: bool = True,
                  limit: int = 50000) -> str:
            """
            stock: Get aggregate bars for a stock over a given date range in custom time window sizes.
            option: Get aggregate bars for a option contract over a given date range in custom time window sizes.
            """
            price_adj_str = "true" if price_adj else "false"
            sort_order = "asc" if sort_asc else "desc"
            url = f"{self.BASE_URL}v2/aggs/ticker/{ticker}/range/{time_scale}/{time_interval}/{start}/{end}?adjusted={price_adj_str}&sort={sort_order}&limit={limit}&{self.api_url}"
            return url

        @staticmethod
        def singleday(self, ticker: str, date: str = dt.now().strftime("%Y-%m-%d"), price_adj: bool = True) -> str:
            """Get the open, close and afterhours prices of a stock symbol on a certain date."""
            price_adj_str = "true" if price_adj else "false"
            url = f"{self.BASE_URL}v1/open-close/{ticker}/{date}?adjusted={price_adj_str}&{self.api_url}"
            return url

        @staticmethod
        def last_trade(self, ticker: str) -> str:
            """
            stock: Get the most recent trade for a given stock.
            option: Get the most recent trade for a given option.
            """
            url = f"{self.BASE_URL}v2/last/trade/{ticker}?{self.api_url}"
            return url

        @staticmethod
        def previous_close(self, ticker: str, price_adj: bool = True):
            """Get the previous day's open, high, low, and close (OHLC) for the specified stock ticker."""
            # hard code:
            version = "v2"
            data_path = "aggs"
            # function fields
            price_adj = "true" if price_adj else "false"
            # url
            req_url = f"{version}/{data_path}/ticker/{ticker}/prev"
            optional_url = f"?adjusted={price_adj}"
            return f"{self.BASE_URL}{req_url}{optional_url}{self.api_url}"

        @staticmethod
        def trades(self, ticker: str, timestamp: str = None, sort_asc: bool = True, limit: int = 50000,
                   sort_by_timestamp: bool = True) -> str:
            """Get trades for a ticker symbol in a given time range."""
            sort_order = "asc" if sort_asc else "desc"
            sort_by = "timestamp" if sort_by_timestamp else ""
            timestamp_str = f"&timestamp={timestamp}" if timestamp is not None else ""
            url = f"{self.BASE_URL}v3/trades/{ticker}?{timestamp_str}&order={sort_order}&limit={limit}&sort={sort_by}&{self.api_url}"
            return url

        @staticmethod
        def quotes(self, ticker: str, timestamp: bool = None, sort_asc: bool = True, limit: int = 50000,
                   sort_by_timestamp: bool = True) -> str:
            """
            stock: Get NBBO quotes for a stock ticker symbol in a given time range.
            option: Get quotes for an option ticker symbol in a given time range.
            """
            # hard code
            data_path = "quotes"
            # url optional
            sort_order = "asc" if sort_asc else "desc"
            sort_by = "timestamp" if sort_by_timestamp else ""
            optional_url = f"?timestamp={timestamp}&order={sort_order}&limit={limit}&sort={sort_by}"
            url = f"{self.BASE_URL}v3/{data_path}/{ticker}{optional_url}&{self.api_url}"
            return url

    class ReferenceData:
        @staticmethod
        def ticker_info(self, ticker: str, date: str = dt.now().strftime("%Y-%m-%d")) -> str:
            """Get a single ticker supported by Polygon.io. This response will have detailed information about the ticker and the company behind it."""
            version = "v3"
            data_path = "reference"
            req_url = f"{version}/{data_path}/tickers/{ticker}"
            if date:
                optional_url = f"?date={date}&"
            else:
                optional_url = "?"  # when date is set to none
            url = f"{self.BASE_URL}{req_url}{optional_url}{self.api_url}"
            return url

        @staticmethod
        def tickers(self, asset_type: str = "CS", market: str = "stocks", active: str = "true", sort: str = "ticker",
                    sort_asc: bool = True, limit: int = 1000) -> str:
            """Query all ticker symbols which are supported by Polygon.io. This API currently includes Stocks/Equities, Crypto, and Forex."""
            data_path = "reference"
            version = "v3"
            req_url = f"{version}/{data_path}/tickers?"
            # options
            sort_order = "asc" if sort_asc else "desc"
            optional_url = f"type={asset_type}&market={market}&active={active}&order={sort_order}&limit={str(limit)}&sort={sort}"
            url = f"{self.BASE_URL}{req_url}{optional_url}&{self.api_url}"
            return url

        @staticmethod
        def news(self, ticker: str, sort_asc: bool = True, limit: int = 1000, sort: str = "published_utc"):
            """Generate the url for news data."""
            version = "v2"
            data_path = "reference"
            sort_order = "asc" if sort_asc else "desc"
            req_url = f"{version}/{data_path}/news?ticker={ticker}"
            optional_url = f"&order={sort_order}&limit={str(limit)}&sort={sort}"
            url = f"{self.BASE_URL}{req_url}{optional_url}&{self.api_url}"
            return url

        @staticmethod
        def marketholiday(self) -> str:
            """Get upcoming market holidays and their open/close times."""
            version = "v1"
            data_path = "marketstatus/upcoming"
            req_url = f"{version}/{data_path}"
            url = f"{self.BASE_URL}{req_url}?{self.api_url}"
            return url

        @staticmethod
        def marketstatus(self) -> str:
            """Returns the URL for the Market Status endpoint"""
            version = "v1"
            data_path = "marketstatus"
            req_url = f"{version}/{data_path}/now"
            optional_url = f"?{self.api_url}"
            url = f"{self.BASE_URL}{req_url}{optional_url}"
            return url

        @staticmethod
        def exchanges(self, asset_class: Optional[str] = "stocks", locale: Optional[str] = "us") -> str:
            """List all exchanges that Polygon.io knows about."""
            version = "v3"
            data_path = "reference"
            req_url = f"{version}/{data_path}/exchanges"
            optional_url = f"?asset_class={asset_class}&locale={locale}"
            url = f"{self.BASE_URL}{req_url}{optional_url}&{self.api_url}"
            return url


class StockUrlFactory(PolyUrlFactory):
    class MarketData(PolyUrlFactory.MarketData):
        @staticmethod
        def last_quote(self, ticker: str) -> str:
            """Get the most recent NBBO (Quote) tick for a given stock."""
            version = "v2"
            data_path = "last/nbbo"
            req_url = f"{version}/{data_path}/{ticker}"
            url = f"{self.BASE_URL}{req_url}?{self.api_url}"
            return url

        @staticmethod
        def marketscan(self, date: str = dt.now().strftime("%Y-%m-%d"), price_adj: bool = True,
                       include_otc: bool = True) -> str:
            """Get the daily open, high, low, and close (OHLC) for the entire us stocks/equities markets."""
            version = "v2"
            data_path = "aggs/grouped/locale/us/market/stocks"
            optional_url = f"{date}?adjusted={str(price_adj).lower()}&include_otc={str(include_otc).lower()}"
            url = f"{self.BASE_URL}{version}/{data_path}/{optional_url}&{self.api_url}"
            return url

        @staticmethod
        def snap_ticker(self, ticker: str) -> str:
            """
            Get the most up-to-date market data for a single traded stock ticker.
            Note: Snapshot data is cleared at 3:30am EST and gets populated as data is received from the exchanges.
            This can happen as early as 4am EST.
            """
            version = "v2"
            data_path = "snapshot/locale/us/markets/stocks/tickers/"
            req_url = f"{version}/{data_path}{ticker}"
            url = f"{self.BASE_URL}{req_url}?{self.api_url}"
            return url

        @staticmethod
        def snap_equitymarket(self, tickers: str = None, include_otc: bool = True) -> str:
            """Get the most up-to-date market data for all traded stock symbols."""
            # hard code
            version = "v2"
            data_path = "snapshot/locale/us/markets/stocks/tickers"
            # create the URL
            req_url = f"{version}/{data_path}"
            optional_url = f"?apiKey={self.api_key}"
            if tickers is not None:
                optional_url += f"&tickers={tickers}"
            if include_otc:
                optional_url += f"&include_otc=true"
            return f"{self.BASE_URL}{req_url}{optional_url}&{self.api_url}"

        @staticmethod
        def snap_gainloss(self, direction_gl: bool = "gainers", include_otc: bool = False) -> str:
            """Get the most up-to-date market data for the current top 20 gainers or losers of the day in the stocks/equities markets."""
            # hard code
            version = "v2"
            direction = "gainers" if direction_gl else "lossers"
            data_path = f"snapshot/locale/us/markets/stocks/{direction}"
            # create the URL
            req_url = f"{version}/{data_path}"
            optional_url = f"?apiKey={self.api_key}"
            if include_otc:
                optional_url += f"&include_otc=true"
            return f"{self.BASE_URL}{req_url}{optional_url}&{self.api_url}"

    class ReferenceData(PolyUrlFactory.ReferenceData):
        @staticmethod
        def stocksplit(self, ticker: str, execution_date: Optional[str] = None, reverse_split: Optional[bool] = None,
                       sort_asc: bool = True, limit: int = 1000, sort: str = "execution_date") -> str:
            """
            Get a list of historical stock splits, including the ticker symbol, the execution date,
            reverse_split: bool, optional (default=None)
                Query for reverse stock splits. A split ratio where split_from is greater than split_to represents a reverse split.
            sort: str, optional (default="execution_date")
                Sort field used for ordering, can be execution_date or ticker
            """
            version = "v3"
            data_path = "reference"
            req_url = f"{version}/{data_path}/splits"
            optional_url = f"?ticker={ticker}"
            sort_order = "asc" if sort_asc else "desc"
            if execution_date:
                optional_url += f"&execution_date={execution_date}"
            if reverse_split is not None:
                optional_url += f"&reverse_split={reverse_split}"
            optional_url += f"&order={sort_order}&limit={limit}&sort={sort}"
            url = f"{self.BASE_URL}{req_url}{optional_url}&{self.api_url}"
            return url

        @staticmethod
        def stock_div(self, ticker: str, sort_asc: bool = True, limit: int = 1000,
                      sort: str = 'ex_dividend_date') -> str:
            """Get a list of historical stock dividends, including the ticker symbol, the ex-dividend date, and the dividend amount."""
            version = "v3"
            data_path = "reference"
            req_url = f"{version}/{data_path}/dividends?ticker={ticker}"
            sort_order = "asc" if sort_asc else "desc"
            optional_url = f"&order={sort_order}&limit={limit}&sort={sort}"
            url = f"{self.BASE_URL}{req_url}{optional_url}&{self.api_url}"
            return url

        @staticmethod
        def financials(self, ticker: str, timeframe: str = "annual", include_sources: bool = True,
                       sort_asc: bool = True, limit: int = 100, sort_by_period: str = True) -> str:
            data_path = "reference/financials"
            # set options
            include_sources = "true" if include_sources else "false"
            sort_order = "asc" if sort_asc else "desc"
            sort_column = "period_of_report_date" if sort_by_period else "filing_date"
            limit_str = str(limit)
            # set optional url parameters
            optional_url = f"?timeframe={timeframe}&include_sources={include_sources}&order={sort_order}&limit={limit_str}&sort={sort_column}"
            url = f"{self.BASE_URL}vX/{data_path}?ticker={ticker}{optional_url}&{self.api_url}"
            return url


class OptionUrlFactory(PolyUrlFactory):
    class MarketData(PolyUrlFactory.MarketData):
        @staticmethod
        def snap_option_contract(self, ticker: str, underlying: str) -> str:
            """Get the snapshot of an option contract for a stock equity."""
            version = "v3"
            data_path = "snapshot/options"
            req_url = f"{version}/{data_path}/{underlying}/{ticker}"
            url = f"{self.BASE_URL}{req_url}?{self.api_url}"
            return url

        @staticmethod
        def snap_option_chain(self, underlying: str, strike_price: Union[float, None] = None,
                              expiration_date: Union[str, None] = None,
                              contract_type: Union[None, Literal["call", "put"]] = None, sort_asc: bool = True,
                              limit: int = 250, sort: Union[
                    Literal["ticker", "expiration_date", "strike_price"]] = "expiration_date") -> str:
            """Get the snapshot of an option contract for a stock equity."""
            version = "v3"
            data_path = "snapshot/options"
            req_url = f"{version}/{data_path}/{underlying}"
            optional_url = ""
            if strike_price is not None:
                optional_url += f"strike_price=str({strike_price})"
            if expiration_date is not None:
                optional_url += f"&expiration_date={expiration_date}"
            if contract_type is not None:
                optional_url += f"&contract_type={contract_type}"
            optional_url += f"&order={'asc' if sort_asc else 'desc'}&limit={limit}&sort={sort}"
            url = f"{self.BASE_URL}{req_url}?{optional_url}&{self.api_url}"
            return url

    class ReferenceData(PolyUrlFactory.ReferenceData):
        @staticmethod
        def options_contract(self, options_ticker: str, as_of: str = dt.today().strftime("%Y-%m-%d")):
            """Get an options contract"""
            version = "v3"
            data_path = f"reference/options/contracts/{options_ticker}"
            req_url = f"{version}/{data_path}"
            params = {}
            if as_of:
                params["as_of"] = as_of
            optional_url = f"{urllib.parse.urlencode(params)}" if params else ""
            url = f"{self.BASE_URL}{req_url}?{optional_url}&{self.api_url}"
            return url

        @staticmethod
        def option_contracts(self, ticker: Union[str,None]=None, underlying_ticker: Union[str,None]=None,
                             contract_type: Union[None, Literal["call", "put"]] = None,
                             expiration_date: Union[str, None] = None, as_of: str = dt.today().strftime("%Y-%m-%d"),
                             strike_price: Union[float, None] = None, expired: Union[None, bool] = None,
                             sort_asc: bool = True, limit: int = 1000,
                             sort: Union[None, Literal[
                                 "ticker", "underlying_ticker", "expiration_date", "strike_price"]] = "underlying_ticker") -> str:
            """Get historical options contracts."""
            version = "v3"
            data_path = "reference/options/contracts"
            req_url = f"{version}/{data_path}"
            params = {
                "limit": limit,
                "sort": sort
            }
            if ticker:
                params["ticker"] = ticker
            if underlying_ticker:
                params["underlying_ticker"] = underlying_ticker
            if contract_type:
                params["contract_type"] = contract_type
            if expiration_date:
                params["expiration_date"] = expiration_date
            params["as_of"] = as_of
            if strike_price:
                params["strike_price"] = strike_price
            if expired is not None:
                params["expired"] = str(expired).lower()
            params["order"] = "asc" if sort_asc else "desc"
            url = f"{self.BASE_URL}{req_url}?{urllib.parse.urlencode(params)}&{self.api_key}"
            return url


class ForexUrlFactory(PolyUrlFactory):
    class MarketData(PolyUrlFactory.MarketData):
        pass

    class ReferenceData(PolyUrlFactory.ReferenceData):
        pass


class CryptoUrlFactory(PolyUrlFactory):
    class MarketData(PolyUrlFactory.MarketData):
        pass

    class ReferenceData(PolyUrlFactory.ReferenceData):
        @staticmethod
        def last_trade_crypto_pair(self, from_symbol: str, to_symbol: str) -> str:
            """Get the last trade tick for a cryptocurrency pair."""
            version = "v1"
            data_path = "last/crypto"
            req_url = f"{version}/{data_path}/{from_symbol}/{to_symbol}"
            url = f"{self.BASE_URL}{req_url}?{self.api_key}"
            return url
