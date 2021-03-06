import os
import pickle
import quandl
quandl.ApiConfig.api_key = 'JJH1Z7c2NDeRw278rr6H'
import numpy as np

def fetch_cosine_values(seq_len, frequency = 0.01, noise = 0.1):
    np.random.seed(101)
    x = np.arange(0.0, seq_len, 1.0) 
    return np.cos(2 * np.pi *frequency * x) + np.random.uniform(low = noise, high = noise, size = seq_len)
    

def date_obj_to_str(date_obj):
    return date_obj.strftime('%Y-%m-%d')


def save_pickle(something, path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, 'wb') as fh:
        pickle.dump(something, fh, pickle.DEFAULT_PROTOCOL)
def load_pickle(path):
    with open(path, 'rb') as fh:
        return pickle.load(fh)

def fetch_stock_price(symbol, from_date, to_date, cache_path='./tmp/prices/'):
    assert from_date <= to_date, "from_date가 to_date보다 큼!"
    
    filename = "{}_{}_{}.pk".format(symbol, str(from_date),str(to_date))
    price_filepath = os.path.join(cache_path, filename)
    
    try:
        prices = load_pickle(price_filepath)
        print("loaded from", price_filepath)
    except IOError:
        historic = quandl.get("WIKI/"+symbol,
                             start_date = date_obj_to_str(from_date),
                             end_date = date_obj_to_str(to_date))
        prices = historic["Adj. Close"].tolist()
        save_pickle(prices, price_filepath)
        print("saved into", price_filepath)
    return prices


def format_dataset(values, temporal_features):
    feat_splits = [values[i:i+temporal_features] for i in range(len(values)-temporal_features)]
    feats = np.vstack(feat_splits) #두 배열을 위에서 아래로 붙이기
    labels = np.array(values[temporal_features:])
    return feats,labels


def matrix_to_array(m):
    return np.asarray(m).reshape(-1)


