import pandas as pd
import os

file_path = os.path.join(os.getcwd(), 'turkish_poems.csv')
df = pd.read_csv(file_path)
data = df['content'].unique()
data = [pair for pair in data if len(pair) <= 1024]

train_size = int(len(data) * 0.8)
train_data = data[:train_size]
test_data = data[train_size:]

with open('train.txt', 'a') as f:

    for pair in train_data:

        f.writelines(pair + '\n')


with open('test.txt', 'a') as f:

    for pair in test_data:

        f.writelines(pair + '\n')


print(len(train_data), len(test_data))
