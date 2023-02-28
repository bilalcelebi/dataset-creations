from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import requests
from tqdm import tqdm
import os

base_url = 'https://www.antoloji.com'
banned_ones = ['javascript:;','None']

def make_request(url):

    headers = {'User-Agent':'My_User_Agent'}
    response = requests.get(url, headers = headers)
    
    if response.status_code == 200:

        return response.text

    else:

        return response.status_code


def get_soup(data):

    return BeautifulSoup(data, 'html.parser')



def get_links(url):

    data = make_request(url)
    soup = get_soup(data)
    
    content = soup.find('ul', {'class':'pd-text-mini'})
    links = content.find_all('div', {'class':'poem-title-pop'})
    links = [link.find('a') for link in links]
    links = [link.get('href') for link in links]
    links = [base_url + link for link in links if link not in banned_ones]
    
    return links



def get_data():
    
    all_links = []

    for i in tqdm(range(2,20)):

        url = f'https://www.antoloji.com/siir/top500/sayfa-{i}/'
        links = get_links(url)

        for link in links:

            if link not in all_links:

                all_links.append(link)

    return all_links


def get_poems():

    links = get_data()
    all_poems = []

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

    filename = 'turkish_popular_poems.csv'
    file_path = os.path.join(os.getcwd(), filename)

    df = pd.Series(data)
    df.to_csv(file_path)

    print(df.shape[0])



def main():

    poems = get_poems()

    save_data(poems)


main()
