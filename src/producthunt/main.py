from api import *
import json
import os

def save_collections(count):

    collections = get_collections(amount = count)
    save_path = '/home/bilalcelebi/Workspace/dataset-creations/src/producthunt/data/collections.json'

    with open(save_path, 'w') as f:
        json.dump(collections, f)

    return f'Collections Data Length : {len(collections)}'


def save_posts(count):

    posts = get_posts(amount = count)
    save_path = '/home/bilalcelebi/Workspace/dataset-creations/src/producthunt/data/posts.json'

    with open(save_path, 'w') as f:
        json.dump(posts, f)

    return f'Posts Data Length : {len(posts)}'


def main():
    
    collection_count = 19
    post_count = 500

    print(save_collections(collection_count))
    sleep(900)
    print(save_posts(post_count))
    print('Done!!! Now run temp.py!')


if __name__ == '__main__':

    main()
