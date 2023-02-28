import fandom
from pprint import pprint
from tqdm import tqdm

fandom.set_wiki('kingkiller')
randoms = fandom.random(pages = 1)
page_id = randoms[1]

page = fandom.page(pageid = page_id)
