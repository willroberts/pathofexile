import jinja2
import requests
import sys
import ujson
from bs4 import BeautifulSoup


class NoItemsFoundException(Exception):
    pass


def get_html(shop_thread_id):
    url = 'http://www.pathofexile.com/forum/view-thread/%s' % shop_thread_id
    html = requests.get(url).content
    html = html.replace('/favicon.ico',
        'http://www.pathofexile.com/favicon.ico')
    html = html.replace('/js/lib/modernizr',
        'http://www.pathofexile.com/js/lib/modernizr')
    return html


def get_javascript(html):
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


class PostIsolator(object):
    ''' Given a shop thread ID, regenerates the page HTML to only show the
    first post while retaining CSS and Javascript. Useful for embedding a
    single post in an iframe.
    '''
    def __init__(self, shop_thread_id):
        self.shop_thread_id = shop_thread_id
        self.html = get_html(self.shop_thread_id)  # original page
        self.soup = BeautifulSoup(self.html)
        self.head_tag = self.soup.find('head')
        self.first_post = self.find_first_post()
        self.javascript = self.find_javascript()
        self.new_html = self.generate_new_html()  # regenerated page

    def find_first_post(self):
        ''' Finds the table of class "forumPostListTable", isolates the first
        row, and then isolates the first column in that row. This leaves only
        the first post of a thread, without the sidebar.
        '''
        post_table = self.soup.find(
            'table',
            attrs={'class': 'forumTable forumPostListTable'}
        )
        return post_table.find_all('tr')[0].find_all('td')[0]

    def find_javascript(self):
        ''' Finds all <script type='text/javascript'> tags in the page, and
        filters out the ones which are already in the <head> tag (and the ones
        which are manually specified below).

        5 is set manually, because we have 2 <script> fields in the <head>
        section, and 3 more hardcoded in PostIsolator.create_test_page().

        This needs some work, to make sure we're picking up javascript in the
        right way. Counting manually isn't very resilient to upstream changes.
        Also need to account for <script src=""> elements, which have no text
        and therefore do nothing when converted to a string.
        '''
        js = self.soup.find_all('script', type='text/javascript')
        new_js = js[5:]
        return ''.join([str(j) for j in new_js])

    def generate_new_html(self):
        ''' Passes the head tag, first post, and javascript into a jinja2
        template to be rendered into a new, complete HTML page.
        '''
        # load the template (post.html)
        jinja2_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                searchpath=['templates', 'pathofexile/templates']
            )
        )
        template = jinja2_env.get_template('post.html')

        # render the template into valid html
        return template.render(
            head_tag = str(self.head_tag),
            first_post = str(self.first_post),
            javascript = self.javascript,
        )
