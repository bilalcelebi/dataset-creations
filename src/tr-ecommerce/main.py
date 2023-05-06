import pandas as pd
import requests
from bs4 import BeautifulSoup as BS
from tqdm import tqdm
import os
import json
from random import randint

def make_request(url):

    response = requests.get(url)

    return response.content


def get_soup(content):

    soup = BS(content, 'html.parser')

    return soup


def get_df():

    data_path = os.path.join(os.getcwd(), 'all_products.csv')
    df = pd.read_csv(data_path)

    return df


def get_links(df):

    links = list(df['product_link'].values)

    return links



def get_details(link):

    content = get_soup(make_request(link))
    container = content.find('ul', {'class':'detail-attr-container'})

    pairs = container.find_all('li', {'class':'detail-attr-item'})
    spans = [pair.find_all('span') for pair in pairs]

    details = []

    for pair in spans:
        texts = []
        for detail in pair:
            texts.append(str(detail.text))

        detail = {texts[0]:texts[1]}
        details.append(detail)
    
    
    details = json.dumps(details, ensure_ascii = False).encode('utf8')

    return details.decode()


if __name__ == '__main__':

    df = get_df()
    

    for i in tqdm(range(int(df.shape[0]))):

        try:
            df.loc[i, 'Metadata'] = get_details(str(df.loc[i, 'product_link']))
        except:
            df.loc[i, 'Metadata'] = None


    df.to_csv('prepared_all_products.csv', index = False)
    print('DONE!!')
