import requests
import ujson
from bs4 import BeautifulSoup


class NoItemsFoundException(Exception):
    pass


def get_html(shop_thread_id):
    ''' ...
    '''
    page_url = 'http://www.pathofexile.com/forum/view-thread/%s' % shop_thread_id
    return requests.get(page_url).content


def get_javascript(html):
    ''' ...
    '''
    soup = BeautifulSoup(html)
    script_tags = soup.find_all('script')

    for javascript in [s.text for s in script_tags]:
        if 'PoE/Item/DeferredItemRenderer' in javascript:
            return javascript
    raise NoItemsFoundException


def get_items(javascript):
    ''' Based on manual inspection, these seem to be the strings to the left
    and the right of the JSON list of items at the end of each shop thread in
    the forum. There may be a more reliable way to access this data.

    :param javascript: ...
    :return: JSON list of items
    '''
    left_bound = 'new R('
    right_bound = ')).run();'
    json_string = javascript.split(left_bound)[1].split(right_bound)[0]
    return [entry[1] for entry in ujson.loads(json_string)]


def find_items(shop_thread_id):
    ''' ...
    '''
    html = get_html(shop_thread_id)
    javascript = get_javascript(html)
    return get_items(javascript)
