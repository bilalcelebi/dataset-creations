import requests
from bs4 import BeautifulSoup as BS
from pprint import pprint
from tqdm import tqdm
from api import get_document
from get_base import get_codes

lang_links = get_codes()

def make_request(url):

    response = requests.get(url)

    if response.status_code == 200:

        return response.content

    else:

        raise 'There is NO data!'


def parse_data(content):

    soup = BS(content, 'html.parser')
    return soup


def find_elements(soup,lang):

    links = soup.find_all('li')
    data = [link.find_all('a') for link in links]
    all_links = []

    for pair in data:
        for link in pair:
            if str(link['href']).startswith('/wiki/'):
                base_url = f'https://{lang}.wikipedia.org'
                wiki_url = base_url + str(link['href'])
                all_links.append(wiki_url)

    return all_links[:-2]


def create_url(pair,lang):

    url = lang_links[str(lang)]
    full = '?from=' + pair
    url = url + str(full)


    return url


def get_last(links,lang):

    last_one = links[-1]
    url = last_one.split(f'https://{lang}.wikipedia.org/wiki/')

    return str(url[1])


def get_titles(pages):

    titles = []

    for page in pages:

        response = make_request(page)
        content = parse_data(response)

        title = content.find('h1', {'class':'firstHeading'})
        title = str(title.text)

        if title not in titles:
            titles.append(title)

    return titles


def get_links(amount,lang):

    all_pages = []

    url = lang_links[str(lang)]

    for i in tqdm(range(int(amount))):

        response = make_request(url)
        parsed_content = parse_data(response)
        links = find_elements(parsed_content,lang)
        
        for link in links:
            if link not in all_pages:
                all_pages.append(link)

        last_one = get_last(links,lang)
        new_url = create_url(last_one,lang)
        url = new_url

    
    all_pages = [str(requests.utils.unquote(page)) for page in all_pages]
    all_pages = [page.split(f'https://{lang}.wikipedia.org/wiki/')[1] for page in all_pages]

    return all_pages
