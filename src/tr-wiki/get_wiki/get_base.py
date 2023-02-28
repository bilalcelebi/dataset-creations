import json


def get_codes():

    data = ''

    with open('codes.json', 'r') as f:
        data = json.loads(f.read())

    codes = []

    for code in data:
        codes.append(str(code['code']))


    urls = dict()

    for code in codes:
        
        url = f'https://{code}.wikipedia.org/wiki/Special:AllPages'
        urls[code] = url

    return urls


