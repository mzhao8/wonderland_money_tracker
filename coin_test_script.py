import coinmarketcapapi
import pickle

def save(file_name, obj):
    with open(file_name, 'wb') as fobj:
        pickle.dump(obj, fobj)

def load(file_name):
    with open(file_name, 'rb') as fobj:
        return pickle.load(fobj)

def get_price(api_key):
    cmc = coinmarketcapapi.CoinMarketCapAPI(api_key)
    data_quote = cmc.cryptocurrency_quotes_latest(slug="wonderland", convert='USD')
    price = data_quote.data['11585']['quote']['USD']['price']

    save("price.pickle", price)

    print(price)