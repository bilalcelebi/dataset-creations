from get_links import get_links
from api import get_document
from tqdm import tqdm
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--amount', required = True)
parser.add_argument('--lang', required = True)

args = parser.parse_args()

pages = get_links(amount = int(args.amount), lang = str(args.lang))
documents = []

for page in tqdm(pages):

    try:
        data = get_document(lang = str(args.lang), document = str(page))
        documents.append(data)
    except:
        pass


df = pd.DataFrame(documents)
df = df.loc[df['content'] != '']
df.to_csv(f'{args.lang}_{len(documents)}_wiki.csv', index = False)
print(f'Oluşturulan Veri Setinin Büyüklüğü : {df.shape}')
