from bs4 import BeautifulSoup
import requests
from time import sleep
from tqdm import tqdm
import os
import pandas as pd

banned_ones = ['javascript:;','None']
base_url = 'https://www.antoloji.com'

def make_request(url):

    headers = {'User-Agent':'My_User_Agent'}
    response = requests.get(url, headers = headers)

    if response.status_code == 200:

        return response.text

    else:

        return 'An Error Occured!!!'


def get_soup(data):

    return BeautifulSoup(data, 'html.parser')

def get_categories():

    url = 'https://www.antoloji.com/siir/konulari/'
    data = make_request(url)
    soup = get_soup(data)

    content = soup.find('div', {'class':'content-bar'})
    links = content.find_all('a')   
    links = [link.get('href') for link in links]
    links = [base_url + str(link) for link in links if link not in banned_ones]
    
    return links


def get_poem_links():
    
    all_links = []
    categories = get_categories()

    for cat in tqdm(categories):

        for i in range(2,8):
            
            try:

                url = f'{cat}sayfa-{i}/'
                data = make_request(url)
                soup = get_soup(data)

                links = soup.find_all('a', {'class':'more-button btn'})
                links = [link.get('href') for link in links]
                links = [base_url + str(link) for link in links if link not in banned_ones]

                for link in links:

                    if link not in all_links:

                        all_links.append(link)
            
            except:

                pass


    return all_links


def get_poems():

    all_poems = []

    links = get_poem_links()

    for link in tqdm(links):
        
        try:

            data = make_request(link)
            soup = get_soup(data)
        
            content = soup.find('div', {'class':'pd-text'})
            pairs = content.find_all('p')
            pairs = [str(pair.get_text()) for pair in pairs]
        
            poem = "".join(pair + '\n' for pair in pairs)

            if poem not in all_poems:

                all_poems.append(poem)
    
        except:

            pass



    return all_poems


def save_data(data):

    filename = 'turkish_poems.csv'
    file_path = os.path.join(os.getcwd(), filename)

    df = pd.Series(data)
    df.to_csv(file_path)
    
    print(df.shape)


def main():

    poems = get_poems()

    save_data(poems)


main()
