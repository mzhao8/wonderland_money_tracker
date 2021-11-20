from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime
import pickle

columns = ['datetime', 'total_staked', 'treasury_balance', 'current_apy', '8_hr_yield', 'price']

def num_clean(x: str):
    x = float(x.text.replace(",","").replace("$","").replace("%",""))
    return x

def load(file_name):
    with open(file_name, 'rb') as fobj:
        return pickle.load(fobj)

with open("test.html") as file:
    page_soup = soup(file, "html.parser")

def update_csv(csv_name):
    df = pd.read_csv(csv_name, header=0)
    df = df[df.columns.intersection(columns)]

    now = datetime.datetime.now()



    numbers_list = page_soup.find_all("p", "landing-footer-item-value")
    numbers_list = list(map(num_clean, numbers_list))

    current_apy_mult = numbers_list[2]/100
    eight_hr_yield = current_apy_mult ** (1/1095)
    numbers_list.append(eight_hr_yield)



    current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    numbers_list.insert(0, current_time)

    current_price = load("price.pickle")
    numbers_list.append(current_price)

    parser_output = dict(zip(columns, numbers_list))
    #print(parser)
    df = df.append(parser_output, ignore_index=True)
    print(df)
    df.to_csv(csv_name)
#print(parser_output)