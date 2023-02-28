from tqdm import tqdm
import pandas as pd
import json
import os

main_path = os.path.join(os.getcwd(), 'factbook.json')
files = []

for folder in os.listdir(main_path):
    for file in os.listdir(os.path.join(main_path, folder)):
        if file.endswith('.json'):
            path = os.path.join(folder, file)
            whole = os.path.join(main_path, path)
            if whole not in files:
                files.append(whole)


def get_data(file):

    data = ''
    
    with open(file, 'r') as f:
        data = f.read()

    data = json.loads(data)

    return data


dataset = []

for file in tqdm(files):

    pair = get_data(file)
    country = ''

    try:
        country = data['Government']['Country name']['conventional short form']['text']
    except:
        country = 'None'
    
    dataset.append(pair)

save_path = os.path.join(os.getcwd(), 'cia_factbook.csv')

df = pd.DataFrame(dataset)
df.to_csv(save_path, index = False)
print(df.shape)
