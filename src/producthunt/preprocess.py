import json
import pandas as pd
import os
from datetime import datetime

collections_path = os.path.join(os.getcwd() + '/data', 'collections.json')
posts_path = os.path.join(os.getcwd() + '/data', 'posts.json')

collections = json.loads(open(collections_path).read())
posts = json.loads(open(posts_path).read())

collections_new = []
posts_new = []

def get_topics(topics):

    nodes = topics['nodes']
    tops = []

    if len(nodes) > 0:

        for topic in nodes:

            tops.append(topic['name'])


    return tops


def get_posts(posts):

    nodes = posts['nodes']
    res = []

    if len(nodes) > 0:

        for node in nodes:

            post = dict()
            post['id'] = node['id']
            post['title'] = node['name']
            post['description'] = node['description']
            post['tagline'] = node['tagline']
            post['reviewsRating'] = node['reviewsRating']
            post['reviewsCount'] = node['reviewsCount']
            post['commentsCount'] = node['commentsCount']
            post['slug'] = node['slug']
            post['topics'] = get_topics(node['topics'])
            post['website'] = node['website']

            res.append(post)

    return res



for col in collections:

    node = dict()

    node['id'] = col['id']
    node['name'] = col['name']
    node['description' ] = col['description']
    node['followersCount'] = col['followersCount']
    node['url'] = col['url']
    node['topics'] = get_topics(col['topics'])
    node['tagline'] = col['tagline']
    node['posts'] = get_posts(col['posts'])
    node['user'] = col['user']['name']

    collections_new.append(node)


def get_comments(comments):

    nodes = comments['nodes']
    res = []

    if len(nodes) > 0:

        for node in nodes:

            comment = dict()
            comment['text'] = node['body']
            comment['votes'] = node['votesCount']

            res.append(comment)


    return res


def process_date(date):

    date = date.split('T')
    date = date[0]
    date = datetime.strptime(date, '%Y-%m-%d')

    return date


for post in posts:

    node = dict()

    node['id'] = post['id']
    node['name'] = post['name']
    node['description'] = post['description']
    node['created_time'] = process_date(post['createdAt'])
    node['rating'] = post['reviewsRating']
    node['reviewsCount'] = post['reviewsCount']
    node['commentsCount'] = post['commentsCount']
    node['tagline'] = post['tagline']
    node['topics'] = get_topics(post['topics'])
    node['slug'] = post['slug']
    node['comments'] = get_comments(post['comments'])
    node['website'] = post['website']

    posts_new.append(node)


collections_df = pd.DataFrame(collections_new)
posts_df = pd.DataFrame(posts_new)

collections_save = os.path.join(os.getcwd() + '/data', 'collections.csv')
posts_save = os.path.join(os.getcwd() + '/data', 'posts.csv')

collections_cols = [col for col in collections_df.columns if collections_df[col].dtype == 'object']
posts_cols = [col for col in posts_df.columns if posts_df[col].dtype == 'object']

for col in collections_cols:

    collections_df[col] = collections_df[col].astype('string')

for col in posts_cols:

    posts_df[col] = posts_df[col].astype('string')


collections_df = collections_df.drop_duplicates()
posts_df = posts_df.drop_duplicates()

collections_df.to_csv(collections_save, index = False)
posts_df.to_csv(posts_save, index = False)

print('Done.')
