import fandom
import pandas as pd
import argparse
from tqdm import tqdm

def get_wiki(name):
    
    try:
        fandom.set_wiki(str(name))
    except:
        raise 'There is no Wiki as named like that.'


def get_page(name):

    search = fandom.search(str(name))
    page = search[0]
    page_id = page[1]

    content = fandom.page(pageid = page_id)
    content = str(content.content)

    return content


def get_random(amount = 1):

    random = fandom.random(amount)
    page = random[0]
    page_id = random[1]

    return page_id


def get_page_by_id(page_id):

    page = fandom.page(pageid = page_id)
    content = page.content
    summary = page.summary

    return {'summary':summary, 'content':content}


def create_bunch(amount = 100):

    page_ids = []

    while len(page_ids) < amount:

        random = get_random()

        if random not in page_ids:

            page_ids.append(random)

        else:

            pass

    
    contents = []

    for page_id in tqdm(page_ids):
        
        try:
            content = get_page_by_id(page_id)
            contents.append(content)
        except:
            pass

    return contents


def save(content, filename):

    df = pd.DataFrame(content)
    df.to_csv(f'{filename}.csv', index = False)
    print(df.shape)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--wiki', required = True)
    parser.add_argument('--amount', required = True)
    
    args = parser.parse_args()

    wiki_name = str(args.wiki)
    amount = int(args.amount)

    get_wiki(wiki_name)
    data = create_bunch(amount)
    save(data, f'fandom_{wiki_name}_dataset')


if __name__ == '__main__':
    main()
