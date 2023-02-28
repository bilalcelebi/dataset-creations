from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import pandas as pd
import os

def make_request(url):
    
    headers = {'User-Agent':'My_User_Agent'}

    response = requests.get(url, headers = headers)

    if response.status_code == 200:

        return response.text

    else:

        return f'Some Error Occurred : {response.status_code}'



def get_links():
    
    url = 'https://www.ideasai.com'

    html_content = make_request(url)

    soup = BeautifulSoup(html_content, 'html.parser')

    links = soup.find_all('a', {'class':'tag-link'})

    links = [url + str(link.get('href')) for link in links]
    
    return links



def extract_contents(link):

    html = make_request(link)

    soup = BeautifulSoup(html, 'html.parser')

    ideas = soup.find_all('h3', {'class':'idea'})

    ideas = [str(idea.text) for idea in ideas]

    return ideas



def get_contents(links):

    contents = []

    for link in tqdm(links):

        response = extract_contents(link)

        for content in response:

            contents.append(content)


    return contents


def main():

    links = get_links()
    contents = get_contents(links[0:1])

    file_path = os.path.join(os.getcwd(), 'ideas.csv')
    
    df = pd.Series(contents)

    df.to_csv(file_path, index = False)
    
    print(df.shape)


main()
