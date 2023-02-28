from mediawiki import MediaWiki
from pprint import pprint
from string import punctuation
import nltk

def get_wiki(lang):
    wiki = MediaWiki(lang = str(lang))
    return wiki

def prepare_text(text):
    
    puncs = ["''","=","==","===","``"]

    for punc in punctuation:
        puncs.append(punc)

    sentences = nltk.sent_tokenize(text)
    sents = []

    for sentence in sentences:

        words = nltk.word_tokenize(sentence)

        words = [word for word in words if word not in puncs]
        words = [word for word in words if len(word) > 1]
        
        sent = ' '.join(word for word in words)
        sent += '.'
        sents.append(sent)


    response = ' '.join(sentence for sentence in sents)

    return response


def get_document(lang,document):

    wiki = get_wiki(lang)
    data = wiki.page(document)
    page = dict()

    page['title'] = data.title
    page['summary'] = prepare_text(str(data.summary))
    page['content'] = prepare_text(str(data.content))

    return page
