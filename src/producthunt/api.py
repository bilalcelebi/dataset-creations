import requests
from time import sleep
from pprint import pprint
from tqdm import tqdm

def make_request(query):

    token = '0J9oSRaHbnm8R4tLoZXaMJAk3P2THjUWA4IJo9B89bY'
    url = 'https://api.producthunt.com/v2/api/graphql'
    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    response = requests.post(url, json={'query': query}, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Query failed to run by returning code of {}. {}'.format(response.status_code, query))
    

def generate_collection(cursor):

    query = """{
        collections(after: "%s") {
            pageInfo {
                endCursor,
                hasNextPage
            },
            nodes {
                id,
                name,
                description,
                followersCount,
                url,
                topics {
                    nodes {
                        name
                    }
                },
                tagline,
                posts {
                    nodes {
                        id,
                        name,
                        description,
                        url,
                        createdAt,
                        tagline,
                        reviewsRating,
                        reviewsCount,
                        commentsCount,
                        slug,
                        website,
                        topics {
                            nodes {
                                name
                            }
                        }
                    }
                },
                user {
                    id,
                    name,
                    isMaker,
                    isViewer,
                    twitterUsername
                }
            }
        }
    }""" % str(cursor)


    return query



def generate_post(cursor):

    query = """{
        posts(after: "%s", order: VOTES) {
            pageInfo {
                endCursor,
                hasNextPage
            },
            nodes {
                id,
                name,
                description,
                url,
                createdAt,
                reviewsRating,
                reviewsCount,
                commentsCount,
                tagline,
                topics {
                    nodes {
                        name
                    }
                },
                comments {
                    nodes {
                        id,
                        body,
                        votesCount
                    }
                },
                website,
                slug
            }
        }
    }""" % str(cursor)


    return query




def get_collections(amount = 10):

    collections = []
    cursor = 'MjA'

    for i in tqdm(range(amount)):
        
        try:

            query = generate_collection(cursor)
            response = make_request(query)
        
            pageinfo = response['data']['collections']['pageInfo']

            if pageinfo['hasNextPage'] == True:

                cursor = str(pageinfo['endCursor'])
        
            else:

                break

            data = response['data']['collections']['nodes']

            for node in data:

                collections.append(node)
            
            sleep(0.5)

        except:

            sleep(905)
            pass


    return collections



def get_posts(amount = 10):

    posts = []
    cursor = 'MjA'

    for i in tqdm(range(amount)):

        try:

            query = generate_post(cursor)
            response = make_request(query)

            pageinfo = response['data']['posts']['pageInfo']

            if pageinfo['hasNextPage'] == True:

                cursor = str(pageinfo['endCursor'])

            else:

                break

            data = response['data']['posts']['nodes']
        
            for node in data:

                posts.append(node)
            
            sleep(0.5)

        except:

            sleep(905)
            pass
    
    return posts


def get_post(post_id):

    query = """{
        post(id: "%s"){
            id,
            name,
            description,
            createdAt,
            reviewsCount,
            reviewsRating,
            commentsCount,
            url,
            tagline,
            slug,
            website,    
            topics {
            nodes {
                name
            }
            },
            user {
            id,
            username,
            twitterUsername      
            },
            comments {
            nodes {
                id,
                body,
                votesCount        
            }
            }
        }
    }
    """ % str(post_id)

    response = make_request(query)
    data = response['data']['post']

    return data


def get_collection(collection_id):

    query = """{
        collection(id: "%s") {
            id,
            name,
            description,
            createdAt,
            followersCount,
            tagline,
            topics {
            nodes {
                name
            }
            },
            user {
            id,
            username,
            twitterUsername
            },
            posts {
            nodes {
                id,
                name,
                description,
                url,
                createdAt,
                reviewsCount,
                reviewsRating,
                commentsCount,
                slug,
                tagline,
                website
            }
            },
            featuredAt
        }
    }
    """ % str(collection_id)

    response = make_request(query)
    data = response['data']['collection']

    return data
