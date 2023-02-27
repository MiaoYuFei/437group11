from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pyarrow import feather
import concurrent.futures
import numpy as np
import scipy.sparse
import itertools
import sys

sys.path.append("D:\Code\peterzergquant\mypolygon")
from poly_getdata import *


@lru_cache()
async def filter_ticker(ticker_lc: List[str]) -> List[str]:
    """
    :param ticker_lc: tickers as list
    :return: filtered tickers as list
    """

    def check_liquidity(stock_df, bench_mark_df):
        missing_dates = bench_mark_df.index[~bench_mark_df.index.isin(stock_df.index)]
        return len(missing_dates) == 0

    output_lc = []
    bench_df = await get_adj_tickers_price(["SPY"])
    ticker_data = await get_adj_tickers_price(ticker_lc)
    if ticker_data.columns.isin(ticker_lc).all():
        if check_liquidity(ticker_data[ticker_lc], bench_df):
            output_lc = ticker_lc
    return output_lc


def knn_news(update_local=False, location="D:/data/raw") -> pd.DataFrame:
    df_snap = feather.read_feather("D:/data/raw/local_snapshot_us_equity")
    news_df = feather.read_feather("D:/data/raw/local_us_equity_news")

    ticker_arr = df_snap.ticker.to_numpy()
    knn_ticker = scipy.sparse.dok_matrix((len(ticker_arr), len(ticker_arr)))
    ticker_maping = {k: v for v, k in enumerate(ticker_arr)}
    target_arr = news_df.tickers.to_numpy()

    def valid_check(tickers, ref):
        return np.isin(tickers, ref)

    def df_modify(tuple_pair, df, ref_map):
        df[ref_map[tuple_pair[0]], ref_map[tuple_pair[1]]] += 1

    # Recommendation 5: Use a better algorithm
    def combo_gen(x):
        def combinations(iterable, r):
            # combinations('ABCD', 2) --> AB AC AD BC BD CD
            # combinations(range(4), 3) --> 012 013 023 123
            pool = tuple(iterable)
            n = len(pool)
            if r > n:
                return
            indices = list(range(r))
            yield tuple(pool[i] for i in indices)
            while True:
                for i in reversed(range(r)):
                    if indices[i] != i + n - r:
                        break
                else:
                    return
                indices[i] += 1
                for j in range(i + 1, r):
                    indices[j] = indices[j - 1] + 1
                yield tuple(pool[i] for i in indices)

        return combinations(x, 2)

    def process_target(x, ref):
        checker = valid_check(x, ref)  # check for invalid tickers
        del_index = np.asarray(np.where(checker == False))
        x = np.delete(x, del_index, axis=0)  # del these invalid tickers
        x_comb = combo_gen(x)
        for pair in x_comb:
            df_modify(pair, knn_ticker, ticker_maping)

    # Recommendation 3: Use multi-threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_target, x) for x in target_arr]
        concurrent.futures.wait(futures)

    knn_df = pd.DataFrame.sparse.from_spmatrix(knn_ticker, columns=ticker_arr, index=ticker_arr)
    if update_local:
        feather.write_feather(knn_df, location + "/local_knn_news")
    return knn_df
