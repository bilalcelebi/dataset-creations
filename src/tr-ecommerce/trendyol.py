from tqdm import tqdm
from bs4 import BeautifulSoup as BS
from price_parser import Price
import pandas as pd
import requests

base_url = 'https://www.trendyol.com'

def make_request(url):

    response = requests.get(url)
    content = BS(response.content, 'html.parser')

    return content


def get_categories():

    content = make_request(base_url)
    categories = content.find_all('a', {'class':'sub-category-header'})
    categories = [str(category['href']) for category in categories]
    categories = [base_url + category for category in categories]

    pairs = content.find_all('ul', {'class':'sub-item-list'})
    links = []

    for pair in pairs:

        urls = pair.find_all('a')
        urls = [str(url['href']) for url in urls]
        urls = [base_url + url for url in urls]

        for url in urls:
            if url not in links:
                links.append(url)


    for link in links:
        if link not in categories:
            categories.append(link)

    
    return categories


def get_cat_urls(cat, amount = 10, company = False):

    urls = []

    for i in range(amount):

        if company == False:
            url = f'{cat}?pi={i + 1}'
        else:
            url = f'{cat}&pi={i + 1}'
      
        if url not in urls:
            urls.append(url)

    return urls


def get_products(cat, amount = 10, company = False):

    urls = None

    if company == False:
        urls = get_cat_urls(cat, amount)
    else:
        urls = get_cat_urls(cat, amount, company = True)

    all_products = []

    for url in urls:

        content = make_request(url)
        container = content.find('div', {'class':'prdct-cntnr-wrppr'})
        pairs = container.find_all('div', {'class':'p-card-chldrn-cntnr card-border'})
        products = []

        for pair in pairs:
            link = pair.find('a')
            link = base_url + str(link['href'])
            if link not in products:
                products.append(link)

        for product in products:
            if product not in all_products:
                all_products.append(product)



    return all_products


def get_product_id(url):

    parsed = url

    if '?' in url:
        new_url = url.split('?')[0]
        parsed = new_url

    product_id = parsed.split('-')[-1]

    return str(product_id)


def get_merchant(content):

    merchant = content.find('a', {'class':'merchant-text'})
    merchant_url = base_url + str(merchant['href'])

    merchant_id = merchant_url.split('-')[-1]
    merchant_id = str(merchant_id)

    merchant_name = str(merchant.text)

    def get_merchant_follower(merchant_id):
        response = requests.get(f'https://public-sdc.trendyol.com/discovery-sellerstore-webgw-service/v1/follow?sellerId={merchant_id}')
        response = response.json()

        return response['count']

    merchant_followers = get_merchant_follower(merchant_id)

    return merchant_url, merchant_id, merchant_name, merchant_followers


def get_product_metadata(content):

    pairs = content.find_all('li', {'class':'detail-attr-item'})
    metadata = dict()

    for pair in pairs:
        spans = pair.find_all('span')
        metadata[str(spans[0].text)] = str(spans[1].text)

    return metadata
    

def get_ratings(product_id, merchant_id, amount = 1):

    url = f'https://public-mdc.trendyol.com/discovery-web-socialgw-service/api/review/{product_id}?merchantId={merchant_id}&storefrontId=1&culture=tr-TR&pageSize=5'
    response = requests.get(url)
    response = response.json()

    ratings_summary = response['result']['contentSummary']['ratingCounts']
    average_rating = float(response['result']['contentSummary']['averageRating'])

    comment_count = response['result']['contentSummary']['totalCommentCount']
    rating_count = response['result']['contentSummary']['totalRatingCount']

    all_parsed_comments = []

    for i in range(amount):

        comment_url = f'https://public-mdc.trendyol.com/discovery-web-socialgw-service/api/review/{product_id}?merchantId={merchant_id}&storefrontId=1&culture=tr-TR&pageSize=5&page={str(i + 1)}'

        comments = requests.get(comment_url)
        comments = comments.json()

        all_comments = comments['result']['productReviews']['content']
        parsed_comments = []

        for comment in all_comments:
            new_comment = dict()

            new_comment['comment'] = comment['comment']
            new_comment['id'] = comment['id']
            new_comment['is_elite'] = comment['isElite']
            new_comment['is_influencer'] = comment['isInfluencer']
            new_comment['rating'] = int(comment['rate'])
            new_comment['liked'] = int(comment['reviewLikeCount'])
            new_comment['seller_name'] = comment['sellerName']
            new_comment['trusted'] = comment['trusted']        
            if 'productSize' in list(comment.keys()):
                new_comment['product_size'] = comment['productSize']
            new_comment['date'] = comment['commentDateISOtype']
            new_comment['title'] = comment['commentTitle']
            new_comment['user_liked'] = comment['userLiked']

            parsed_comments.append(new_comment)

        for comment in parsed_comments:
            if comment not in all_parsed_comments:
                all_parsed_comments.append(comment)


    data = {
        "ratings_summary":ratings_summary,
        "average_rating":average_rating,
        "comment_count":comment_count,
        "rating_count":rating_count,
        "comments":all_parsed_comments
    }

    return data


def get_questions(product_id, merchant_id, amount = 1):

    all_questions = []

    for i in range(amount): 

        url = f'https://public-mdc.trendyol.com/discovery-web-socialgw-service/api/questions/answered/filter?page={str(i + 1)}&tag=tümü&sellerId={merchant_id}&contentId={product_id}'
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            questions = response['result']['content']

            for question in questions:
                if question not in all_questions:
                    all_questions.append(question)


    prepared_questions = []

    for question in all_questions:

        new = dict()

        new['id'] = question['id']
        new['question'] = question['text']
        new['merchant_id'] = question['merchantId']
        new['merchant_name'] = question['merchantName']
        new['answer'] = question['answer']['text']
        
        time_range = str(question['answeredDateMessage'])
        replied_time = time_range.split(' ')[0]
        replied_time = int(replied_time)
        range_type = None

        if 'saat' in time_range:
            replied_time = replied_time * 60
        elif 'gün' in time_range:
            replied_time = replied_time * 24 * 60

        new['replied_time'] = replied_time

        if new not in prepared_questions:
            prepared_questions.append(new)

    
    return prepared_questions



def get_product_details(url):

    content = make_request(url)

    title_box = content.find('h1', {'class':'pr-new-br'})
    title = str(title_box.find('span').text)

    price = str(content.find('span', {'class':'prc-dsc'}).text)
    price = Price.fromstring(price)
    price = float(price.amount)

    product_id = get_product_id(url)

    merchant = get_merchant(content)
    merchant_id = merchant[1]
    merchant_name = merchant[2]
    merchant_url = merchant[0]
    merchant_followers = merchant[3]

    metadata = get_product_metadata(content)
    
    ratings_and_comments = get_ratings(product_id, merchant_id)
    average_rating = ratings_and_comments['average_rating']
    comment_count = ratings_and_comments['comment_count']
    rating_count = ratings_and_comments['rating_count']
    comments = ratings_and_comments['comments']
    ratings_summary = ratings_and_comments['ratings_summary']

    questions = get_questions(product_id, merchant_id)

    categories = content.find_all('a', {'class':'product-detail-breadcrumb-item'})
    categories = [str(category.text) for category in categories if str(category.text) != 'Anasayfa']
    prepared_cats = []
    for category in categories:
        if category not in prepared_cats:
            prepared_cats.append(category)
    del prepared_cats[-1]

    data = {
        "product_link":url,
        "product_id":product_id,
        "price":price,
        "title":title,
        "categories:":prepared_cats,
        "ratings_summary":ratings_summary,
        "average_rating":average_rating,
        "comment_count":comment_count,
        "rating_count":rating_count,
        "comments":comments,
        "questions":questions,
        "merchant_id":merchant_id,
        "merchant_name":merchant_name,
        "merchant_website":merchant_url,
        "merchant_follower":merchant_followers,
        "metadata":metadata
    }

    return data


def get_company(company, amount):

    url = f'https://www.trendyol.com/sr?q={company}&qt={company}&st={company}&os=1'
    products = get_products(url, int(amount), company = True)
    details = []

    for product in tqdm(products):
        details.append(get_product_details(product))

    df = pd.DataFrame(details)
    df.to_csv('products.csv', index = False)

    return df.shape


def create_dataset(amount):

    categories = get_categories()
    all_products = []

    for category in tqdm(categories):

        try:
            products = get_products(category, amount, company = False)
            for product in products:
                if product not in all_products:
                    all_products.append(product)
        except:
            pass


    details = []

    for product in tqdm(all_products):
        details.append(get_product_details(product))


    df = pd.DataFrame(details)
    df.to_csv('dataset.csv', index = False)

    return df.shape




if __name__ == '__main__':

    ## You can create dataset by all categories or you can create dataset by brand or company
    ## just use the 2 functions above

    # print(get_company(company_name, amount)) - Give brand name and amount value
    # print(create_dataset(10)) - give amount value