from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime
import pickle

columns = ['coin', 'datetime', 'total_staked', 'treasury_balance', 'current_apy', '8_hr_yield', 'price']

def num_clean(x: str):
    x = float(x.text.replace(",","").replace("$","").replace("%","").replace(" SB","").replace(" Days", ""))
    return x

def load(file_name):
    with open(file_name, 'rb') as fobj:
        return pickle.load(fobj)



def update_csv_wonderland(csv_name):
    df = pd.read_csv(csv_name, header=0)
    df = df[df.columns.intersection(columns)]

    with open("wonderland.html") as file:
        page_soup = soup(file, "html.parser")

    now = datetime.datetime.now()

    numbers_list = page_soup.find_all("p", "landing-footer-item-value")
    numbers_list = list(map(num_clean, numbers_list))

    current_apy_mult = numbers_list[2]/100
    eight_hr_yield = current_apy_mult ** (1/1095)
    numbers_list.append(eight_hr_yield)

    current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    numbers_list.insert(0, current_time)

    numbers_list.insert(0, "wonderland")

    current_price = load("wonderland_price.pickle")
    numbers_list.append(current_price)

    parser_output = dict(zip(columns, numbers_list))
    #print(parser)
    df = df.append(parser_output, ignore_index=True)
    print(df)
    df.to_csv(csv_name)
#print(parser_output)

def update_csv_snowbank(csv_name):
    df = pd.read_csv(csv_name, header=0)
    df = df[df.columns.intersection(columns)]

    with open("snowbank.html") as file:
        page_soup = soup(file, "html.parser")

    now = datetime.datetime.now()

    numbers_list = page_soup.find_all("p", "card-value")
    numbers_list = list(map(num_clean, numbers_list))
    # sb price, sb market cap, sb tvl, sb apy, sb index, sb treasury balance, sb backing per sb, runway
    current_price = numbers_list[0]
    total_staked = numbers_list[2]
    treasury_balance = numbers_list[5]
    current_apy_mult = numbers_list[3]/100
    eight_hr_yield = current_apy_mult ** (1/1095)
    current_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    numbers_list = ["snowbank", current_time, total_staked, treasury_balance, current_apy_mult, eight_hr_yield, current_price]


    parser_output = dict(zip(columns, numbers_list))
    #print(parser)
    df = df.append(parser_output, ignore_index=True)
    print(df)
    df.to_csv(csv_name)