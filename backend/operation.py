#base imports
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)
poly_dir = os.path.abspath(os.path.join(os.getcwd(), 'data_poly'))
sys.path.append(poly_dir)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import itertools
import concurrent.futures

# package imports
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
from tqdm import tqdm
import pyarrow.feather as feather
import pickle
from firebase_helper import *
import math
import asyncio
from pandas.io.json import json_normalize
import hashlib
from google.cloud.firestore_v1 import Query
import nest_asyncio
nest_asyncio.apply()
from IPython.display import display
from concurrent.futures import ThreadPoolExecutor
import datetime
import pytz
from dotenv import load_dotenv

# local imports
import data_poly.poly_getdata as poly_getdata
import data_poly.poly_url as poly_url
import data_poly.poly_helper as poly_helper


# Suppress the UserWarning with a specific message
warnings.filterwarnings(
    "ignore",
    message="DataFrame columns are not unique, some columns will be omitted.",
    category=UserWarning
)

        
#upload functions
def cloud_upload_single(db, collection_name, doc_name, data_dict):
    #upload data to db
    doc_ref = db.collection(collection_name).document(doc_name)
    doc_ref.set(data_dict)

def chunks(data, size):
    data_keys = list(data.keys())
    for i in range(0, len(data_keys), size):
        yield {k: data[k] for k in data_keys[i:i+size]}
        
def cloud_upload_seq(db, collection_name, data_dict, chunk_size=500):
    sub_dicts = list(chunks(data_dict, chunk_size))
    # Iterate through the sub_dicts
    for sub_dict in sub_dicts:
        # Create a batch to batch the writes
        batch = db.batch()
        # Iterate through the key-value pairs in the sub_dict
        for key, value in sub_dict.items():
            # Set the document reference in the news_data collection using the key
            doc_ref = db.collection(collection_name).document(str(key))
            # Add the key-value pair to the batch
            batch.set(doc_ref, value)
        # Commit the batch
        batch.commit()
        
async def set_document(doc_ref, data):
    with ThreadPoolExecutor() as executor:
        await asyncio.get_event_loop().run_in_executor(executor, doc_ref.set, data)

async def write_document(doc_ref, data):
    """
    a coroutine for writing a document to Firestore
    """
    await set_document(doc_ref, data)

async def write_batch(batch, collection_name, task_limit=12):
    """
    write a batch of documents to Firestore asynchronously
    """
    semaphore = asyncio.Semaphore(task_limit) # Create a semaphore to limit the number of concurrent tasks
    coroutines = [] # Create a list to hold the coroutines
    # Iterate through the batch and create a coroutine for each document
    for key, value in batch.items():
        # Set the document reference in the news_data collection using the key
        doc_ref = db.collection(collection_name).document(str(key))
        # Create a coroutine to write the document to Firestore
        coroutine = write_document(doc_ref, value)
        # Append the coroutine to the list
        coroutines.append(coroutine)
    # Run the coroutines concurrently with the semaphore
    async with semaphore:
        await asyncio.gather(*coroutines)

async def cloud_upload(db, data_dict, collection_name, chunk_size=500, task_limit=12):
    """
    upload data dict to collection
    """
    sub_dicts = list(chunks(data_dict, chunk_size))
    
    # Create a progress bar for displaying the progress
    progress_bar = tqdm(total=len(sub_dicts), desc="Uploading")
    display(progress_bar)

    # Iterate through the sub_dicts
    for sub_dict in sub_dicts:
        batch = {}  # Create a batch to batch the writes
        for key, value in sub_dict.items():  # Iterate through the key-value pairs in the sub_dict
            batch[key] = value  # Add the key-value pair to the batch
        await write_batch(batch, collection_name, task_limit=task_limit)  # Run the write_batch coroutine asynchronously
        progress_bar.update(1)  # Update the progress bar

    progress_bar.close()  # Close the progress bar when done
        
        
def delete_collection(db, collection_path, batch_size=500):
    """
    Delete all documents in a collection in batches to avoid exceeding the maximum write rate or request size limit.
    """
    query = db.collection(collection_path).limit(batch_size) # Create a query for the collection
    has_docs = True # Set a flag to determine if the loop should continue
    while has_docs: # Delete documents in batches until no more documents exist
        docs = query.stream() # Get a batch of documents
        has_docs = False # Set has_docs to False, assuming there are no more documents
        batch = db.batch() # Create a batch to delete documents
        for doc in docs: # Iterate through documents and delete them in the batch
            batch.delete(doc.reference)
            has_docs = True # If a document is found, set has_docs to True
        batch.commit() # Commit the batch
        if not has_docs: # If no documents were found, break out of the loop
            break

#sic matching and ticker map cloud set

def cloud_upload_ticker_map(db):
    """
    upload and set ticker map (str->int) to cloud firestore 
    """
    ticker_map_path = "/mnt/d/data/news/ticker_maping_dict.pkl"
    ticker_map_dict = pickle.load(open(ticker_map_path, "rb"))
    #overwrite ticker mapping on db
    doc_ref = db.collection('ticker_map').document('dict')
    doc_ref.set(ticker_map_dict)

def memoize(function):
    """
    cache helper for speed optimization
    """
    cache = {}
    def wrapper(input):
        if input not in cache:
            cache[input] = function(input)
        return cache[input]
    return wrapper

@memoize
def sic_match(input):
    """
    takes a SIC code and return the 10 SIC industries string
    """
    sic_codes = {
        '01': 'agriculture',
        '02': 'agriculture',
        '07': 'agriculture',
        '08': 'agriculture',
        '09': 'agriculture',
        '10': 'mining',
        '11': 'mining',
        '12': 'mining',
        '13': 'mining',
        '14': 'mining',
        '15': 'construction',
        '16': 'construction',
        '17': 'construction',
        **{f"{i:02d}": "manufacturing" for i in range(20, 40)},
        **{f"{i:02d}": "transportation" for i in range(40, 50)},
        '50': 'wholesale',
        '51': 'wholesale',
        **{f"{i:02d}": "retail" for i in range(52, 60)},
        **{f"{i:02d}": "finance" for i in range(60, 68)},
        **{f"{i:02d}": "services" for i in range(70, 90)},
        **{f"{i:02d}": "public_administration" for i in range(91, 100)},
    }
    try:
        return sic_codes[str(input)[0:2]]
    except KeyError:
        raise ValueError("Invalid input. Please enter a two-character string matching a valid SIC code.")
        
#generate ticker info dict

async def get_all_ticker_info(db):
    ticker_map_dict = db.collection('tickers').document('ticker_hash').get().to_dict()
    url_factory = poly_url.StockUrlFactory(api_key)
    ticker_lc = ticker_map_dict.keys()
    urls_dict = {ticker: url_factory.ReferenceData.ticker_info(url_factory, ticker) for ticker in ticker_lc}
    df_dict = await poly_helper.get_data_from_urls(urls_dict)
    return df_dict

async def ticker_info_ready(db):
    df_info_dict = await get_all_ticker_info(db)
    upsert_dict = {ticker: df.to_dict('records')[0] for ticker, df in df_info_dict.items()}
    return upsert_dict

def info_dict_to_sic_map(ticker_info_dict, ticker_hash_dict):
    sic_map_dict = {
        ticker_hash_dict[str(ticker)]: sic_match(info["sic_code"][:2]) if ("sic_code" in info.keys()) else None
        for ticker, info in ticker_info_dict.items()
    }
    return sic_map_dict

# upload news data to db

def convert_arrays_to_lists(value):
    """
    Convert arrays to lists
    """
    if isinstance(value, (list, np.ndarray)):
        return list(value)
    return value

def to_boolean_list(industries):
    """
    convert the industries list to a boolean list
    """
    global industry_cols
    return [col in industries for col in industry_cols]

def clean_news(news_data=pd.read_feather("/mnt/d/data/news/local_us_equity_news")):
    """depreciated"""
    cols_to_process = ['tickers', 'keywords']
    for col in cols_to_process:
        news_data[col] = news_data[col].apply(lambda lst:  tuple(lst) if isinstance(lst, list) else None)
    if "publisher" in news_data.columns:
        flattened_info=json_normalize(news_data["publisher"])
        flattened_info.reset_index(drop=True, inplace=True)
        news_data.reset_index(drop=True, inplace=True)
        news_data=pd.concat([news_data.drop('publisher', axis=1), flattened_info], axis=1)
    news_data.drop_duplicates(inplace=True)
    return news_data

def apply_industries(news_data):
    global hash_sic_dict,ticker_hash_dict
    #add 10 industry cols
    news_data["industries"] = news_data.tickers.apply(lambda tickers: [hash_sic_dict.get(ticker_hash_dict.get(ticker,None), None) for ticker in tickers])
    news_data["industries"] = news_data["industries"].apply(lambda lst:  tuple(lst) if lst is not None else None)
    # Define the industry column names and default values
    industry_cols = list(set(['agriculture', 'mining', 'construction', 'manufacturing', 'transportation',
                     'wholesale', 'retail', 'finance', 'services', 'public_administration']))
    # Create a dataframe with the boolean values for each industry
    boolean_df = pd.DataFrame(tqdm(news_data['industries'].apply(to_boolean_list).tolist()), columns=industry_cols)
    # process the news_data df
    news_data = news_data.reset_index(drop=True)
    boolean_df = boolean_df.reset_index(drop=True)
    news_data = pd.concat([news_data, boolean_df], axis=1)
    news_data = news_data.applymap(convert_arrays_to_lists)
    return news_data

def process_news_data():
    global db
    news_data = clean_news()
    #get mapping dict
    doc_ref = db.collection('tickers').document('hash_sic') # Get reference to the document
    hash_sic_doc = doc_ref.get() # Retrieve the document data
    hash_sic_dict = hash_sic_doc.to_dict() if hash_sic_doc.exists else print(f"No such document: {doc_ref.id}") # Check if the document exists
    doc_ref = db.collection('tickers').document('ticker_hash') # Get reference to the document
    ticker_hash_doc = doc_ref.get() # Retrieve the document data
    ticker_hash_dict = ticker_hash_doc.to_dict() if ticker_hash_doc.exists else print(f"No such document: {doc_ref.id}") # Check if the document exists
    return apply_industries(news_data, hash_sic_dict,ticker_hash_dict)

def news_data_to_dict(news_data):
    # Convert the DataFrame to a dictionary format
    news_data_dict = news_data.set_index('id').T.to_dict()
    return news_data_dict

def gen_10_industries_df():
    global news_data_dict, industry_cols
    industry_data = {} # Create a dictionary to hold the smaller dataframes for each industry
    for industry_col in industry_cols: # Iterate through the industry columns
        industry_news = {} # Create a dictionary to hold the most recent 100 news items for this industry
        for news_hash_id, news_data in news_data_dict.items(): # Iterate through all news items
            industries = news_data.get('industries', [])
            if industry_col in industries: # Check if the news item belongs to the current industry
                industry_news[news_hash_id] = news_data # Add the news item to the industry_news dictionary
        industry_news = dict(sorted(industry_news.items(), key=lambda x: x[1]['published_utc'], reverse=True)[:100]) # Sort the dictionary by published_utc and take the most recent 100 items
        industry_data[industry_col] = industry_news # Add the industry_news dictionary to the industry_data dictionary
        #print(f"{industry_col}: {len(industry_news)} rows added")
    return industry_data

def target_ticker_pair_gen(news_data_dict, ticker_hash_dict):
    target_data_dict = {
        key: tuple(
            itertools.combinations(
                tuple(
                    ticker_hash_dict.get(ticker, None)
                    for ticker in value['tickers']
                    if ticker_hash_dict.get(ticker, None) is not None
                ),
                2
            )
        )
        for key, value in news_data_dict.items()
    }
    # Flatten target_data
    target_data = tuple(itertools.chain.from_iterable(target_data_dict.values()))
    return target_data

def knn_gen(target_data, hash_sic_dict, ticker_hash_dict):
    knn_dict = {key: {inner_key: 0 for inner_key in hash_sic_dict} for key in hash_sic_dict}
    for pair in tqdm(target_data):
        first_item, second_item = pair
        knn_dict[first_item][second_item] += 1
        knn_dict[second_item][first_item] += 1
    return knn_dict

def ticker_map_dict_gen():
    # Define a function to create the hashid
    def create_hashid(row):
        cik = row['cik'] if row['cik'] else ''
        composite_figi = row['composite_figi'] if row['composite_figi'] else ''
        hash_str = f"{row['ticker']}{cik}{composite_figi}"
        return hashlib.md5(hash_str.encode()).hexdigest()

    #get tickers on us equity market:
    url_factory = poly_url.StockUrlFactory(api_key)
    url = url_factory.ReferenceData.tickers(url_factory)
    tickers =  poly_helper.get_data_from_single_url(url)
    # Apply the function to each row to create a hashid column
    tickers['hashid'] = tickers.apply(create_hashid, axis=1)
    ticker_map_dict = tickers[['ticker', 'hashid']].set_index('ticker').to_dict()['hashid']
    return ticker_map_dict

def user_base_pref_gen():
    global db, hash_sic_dict
    user_pref_docs = db.collection('user_preferences').stream()  # Get all documents from the user_preference collection
    user_ticker_pref_dict = {}  # Initialize an empty dictionary to store user preferences for each ticker
    for doc in user_pref_docs:  # Iterate through each user preference document
        user_id = doc.id
        user_pref = doc.to_dict()  # Get the user preference dictionary from the document data
        pref_dict = {key: 0 for key in hash_sic_dict} # Initialize a new pref_dict with the same keys as hash_sic_dict and default values of 0
        # loop
        for pref_industry, pref_value in user_pref.items():
            for ticker_hash_id, sic_code in hash_sic_dict.items():
                if sic_code == pref_industry:
                    if pref_value==True:
                        pref_dict[ticker_hash_id] += 1
                    else:
                        pref_dict[ticker_hash_id] -= 1
        # Store the pref_dict in user_ticker_pref
        user_ticker_pref_dict[user_id] = pref_dict
    return user_ticker_pref_dict

def get_industry_news():
    global db, industry_news_dict
    news_datetime_dict = {news_hash_id: datetime.datetime.fromisoformat(news_data['published_utc'][:-1]).replace(tzinfo=pytz.UTC)
                      for industry_data in industry_news_dict.values() for news_hash_id, news_data in industry_data.items()}
    result_dict = {}
    for sub_dict in industry_news_dict.values():
        result_dict.update(sub_dict)
    return result_dict, news_datetime_dict

def industry_news_to_hash():
    global industry_news_compiled_dict, ticker_hash_dict
    return {
        key: {ticker_hash_dict.get(ticker) for ticker in value["tickers"] if ticker_hash_dict.get(ticker)}
        for key, value in industry_news_compiled_dict.items()
    }

def pref_score_gen():
    global industry_news_hash_dict,user_ticker_pref_dict
    preference_scores = {} # Initialize a dictionary to store preference scores for each news article and user
    for news_hash_id, ticker_hash_ids in industry_news_hash_dict.items(): # Iterate through each news article and its associated tickers
        for user_hash_id, user_pref_dict in user_ticker_pref_dict.items(): # Iterate through each user and their associated preference dictionary
            user_article_scores = [] # Initialize a list to store preference scores for this user and article
            for ticker_hash_id in ticker_hash_ids: # Iterate through each ticker in the article's ticker list
                pref_score = user_pref_dict.get(ticker_hash_id, 0) # Lookup the preference score for this ticker for the current user
                user_article_scores.append(pref_score) # Add the preference score to the list for this article
            avg_score = sum(user_article_scores) / len(user_article_scores) # Calculate the average preference score for this user and article
            if news_hash_id not in preference_scores: # Store the preference score in the dictionary
                preference_scores[news_hash_id] = {}
            preference_scores[news_hash_id][user_hash_id] = avg_score
    return preference_scores
        
def flip_dict(dict1):
    dict2 = {}
    for parent_key, sub_dict in dict1.items():
        for sub_key, sub_value in sub_dict.items():
            if sub_key not in dict2:
                dict2[sub_key] = {}
            dict2[sub_key][parent_key] = sub_value
    return dict2

def scale_pref_scores(preference_scores):
    global news_datetime_dict
    now_utc = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    for news_hash_id, news_datetime in news_datetime_dict.items(): # Loop over all news articles
        delta_time = (now_utc - news_datetime).total_seconds() # Compute the time difference between the article and the current time in seconds
        scale_factor = min(1, 4/np.log1p(delta_time)) # Compute the scaling factor
        for user_hash_id in preference_scores[news_hash_id]: # Loop over all users for this news article
            if preference_scores[news_hash_id][user_hash_id] !=0:
                preference_scores[news_hash_id][user_hash_id] *= scale_factor # Scale the preference score for this ticker
    return preference_scores

def sort_subdict_by_value(d):
    return {k: dict(sorted(v.items(), key=lambda x: x[1], reverse=True)) for k, v in d.items()}

def get_user_news_rank():
    preference_scores = pref_score_gen()
    preference_scores = scale_pref_scores(preference_scores)
    preference_scores_user_rank = flip_dict(preference_scores)
    preference_scores_user_rank = sort_subdict_by_value(preference_scores_user_rank)
    return preference_scores_user_rank

def apply_industries(news_data_dict, hash_sic_dict, ticker_hash_dict):
    industry_cols = list(set(['agriculture', 'mining', 'construction', 'manufacturing', 'transportation',
                              'wholesale', 'retail', 'finance', 'services', 'public_administration']))
    for news_hash_id, news_data in news_data_dict.items():
        tickers = news_data.get('tickers', [])
        industries = [hash_sic_dict.get(ticker_hash_dict.get(ticker, None), None) for ticker in tickers]
        news_data['industries'] = tuple(industries) if industries else None
        boolean_values = to_boolean_list(news_data['industries'])
        news_data.update({col: val for col, val in zip(industry_cols, boolean_values)})
    return news_data_dict

async def get_news_dict(ticker_hash_dict):
    url_factory = poly_url.StockUrlFactory(api_key)
    ticker_lc = ticker_hash_dict.keys()
    doc_ref = db.collection("#update_time").document("data_update") # Get reference to the document
    t0_update = doc_ref.get() # Retrieve the document data
    update_date = t0_update.get("time")  # assuming the date field in the document is called "date"
    date_str = update_date.strftime("%Y-%m-%d")
    urls_dict = {ticker: url_factory.ReferenceData.news(url_factory, ticker, publish_utc_gte=date_str) for ticker in ticker_lc}
    news_dict = await poly_helper.get_data_from_urls(urls_dict)
    recent_news_df = pd.concat(news_dict)
    recent_news_df.reset_index(inplace=True,drop=True)
    recent_news_df = clean_news(recent_news_df)
    recent_news_df.set_index('id', inplace=True)
    return recent_news_df.T.to_dict()
    
def update_news_data_dict(news_data_dict, recent_news_dict):
    news_data_dict.update(recent_news_dict)
    return dict(sorted(news_data_dict.items(), key=lambda x: x[1]["published_utc"], reverse=True))

async def run_news_update():
    global news_data_dict, ticker_hash_dict, hash_sic_dict
    recent_news_dict = await get_news_dict(ticker_hash_dict)
    recent_news_dict = apply_industries(recent_news_dict, hash_sic_dict, ticker_hash_dict)
    news_data_dict = update_news_data_dict(news_data_dict, recent_news_dict)
    return news_data_dict

def show_n_item_in_dict(mydict,n=1):
    if n>0:
        return {k: v for idx, (k, v) in enumerate(mydict.items()) if idx < 1}
    elif n<0:
        return {k: news_data_dict[k] for k in list(news_data_dict)[-1:]}
    else:
        print("n can't be 0")
        
def get_key_by_value(d, value):
    for k, v in d.items():
        if v == value:
            return k
    return None


#frequent updates:
async def frequent_update():
    global news_data_dict, industry_news_dict, user_ticker_pref_dict, industry_news_compiled_dict, news_datetime_dict, industry_news_hash_dict, preference_scores_user_rank
    #gen updated news
    news_data_dict = await run_news_update()
    #gen industry news
    industry_news_dict = gen_10_industries_df()
    #gen user_ticker_pref
    user_ticker_pref_dict = user_base_pref_gen()
    industry_news_compiled_dict, news_datetime_dict = get_industry_news()
    industry_news_hash_dict = industry_news_to_hash()
    #gen user_news_rank
    preference_scores_user_rank = get_user_news_rank()
    #uploads
    await upload_industry_data()
    await upload_user_ticker_pref()
    await upload_preference_scores_user_rank()
    upload_time_tracker()
    
async def upload_industry_data():
    global db, industry_news_dict
    await cloud_upload(db, industry_news_dict, "industry_data")
    total_news_dict = flatten_dict(industry_news_dict)
    await cloud_upload(db, total_news_dict, "recent_news")
    
async def upload_user_ticker_pref():
    global db, user_ticker_pref_dict
    await cloud_upload(db, user_ticker_pref_dict, "user_ticker_pref")
    
async def upload_preference_scores_user_rank():
    global db, preference_scores_user_rank
    await cloud_upload(db, preference_scores_user_rank, "preference_scores_user_rank")
    
def upload_time_tracker(full_update=True):
    global db
    if full_update:
        cloud_upload_single(db, "#update_time", "data_update", {"time":datetime.datetime.now()})
    else:
        cloud_upload_single(db, "#update_time", "user_pref_update", {"time":datetime.datetime.now()})

def upload_ticker_info(db):
    global ticker_info_dict
    cloud_upload_seq(db, "ticker_info", ticker_info_dict)
    
async def upload_new_user_pref():
    global news_data_dict, industry_news_dict, user_ticker_pref_dict, industry_news_compiled_dict, news_datetime_dict, industry_news_hash_dict, preference_scores_user_rank
    user_ticker_pref_dict = user_base_pref_gen()
    industry_news_compiled_dict, news_datetime_dict = get_industry_news()
    industry_news_hash_dict = industry_news_to_hash()
    preference_scores_user_rank = get_user_news_rank()
    #upload data
    await upload_user_ticker_pref()
    await upload_preference_scores_user_rank()
    upload_time_tracker(full_update=False)

            
async def main():
    #read local
    # Loop over the object names
    load_dotenv(dotenv_path="/home/peterzerg/repos/quant/.ENV")
    api_key = os.environ.get("POLYGON_APIKEY_MASTER")
    fb = firebase_helper()
    db = fb.get_db()

    #project global vars
    industry_cols= ['agriculture', 'mining', 'construction', 'manufacturing', 'transportation','wholesale', 'retail', 'finance', 'services', 'public_administration']
    object_names = ['ticker_hash_dict','hash_sic_dict','news_data_dict','knn_dict','user_ticker_pref_dict','ticker_info_dict','industry_news_dict','industry_news_compiled_dict',
                    'news_datetime_dict','industry_news_hash_dict','preference_scores_user_rank']

    for name in tqdm(object_names):
        # Load the object by name
        with open(f'{name}.pickle', 'rb') as f:
            globals()[name] = pickle.load(f)
            
    await frequent_update()
    
    #save local
    # Loop over the object names
    for name in tqdm(object_names):
        # Load the object by name
        obj = globals()[name]
        # Save the object as a pickle file using the name
        with open(f'{name}.pickle', 'wb') as f:
            pickle.dump(obj, f)
    
            
if __name__ == "__main__":
    main()