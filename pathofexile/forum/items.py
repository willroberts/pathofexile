import requests
import ujson
from bs4 import BeautifulSoup


class NoItemsFoundException(Exception):
    pass


def get_html(shop_thread_id):
    url = 'http://www.pathofexile.com/forum/view-thread/%s' % shop_thread_id
    html = requests.get(url).content
    html = html.replace(
        '/favicon.ico',
        'http://www.pathofexile.com/favicon.ico',
    )
    html = html.replace(
        '/js/lib/modernizr',
        'http://www.pathofexile.com/js/lib/modernizr',
    )
    return html


def get_items(html):
    ''' Based on manual inspection, these seem to be the strings to the left
    and the right of the JSON list of items at the end of each shop thread in
    the forum. There may be a more reliable way to access this data.

    :param html: the html content of a forum shop thread
    :return: list of item dictionaries
    '''
    # find relevant javascript
    soup = BeautifulSoup(html)
    script_tags = soup.find_all('script')
    items_code = None
    for js in [s.text for s in script_tags]:
        if 'PoE/Item/DeferredItemRenderer' in js:
            items_code = js
    if items_code is None:
        raise NoItemsFoundException

    # parse javascript
    left_bound = 'new R('
    right_bound = ')).run();'
    json_string = javascript.split(left_bound)[1].split(right_bound)[0]
    return [entry[1] for entry in ujson.loads(json_string)]
