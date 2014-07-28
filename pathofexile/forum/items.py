import jinja2
import logging
import requests
import ujson
from bs4 import BeautifulSoup

logging.basicConfig(filename='item_server.log', level=logging.DEBUG)


class NoItemsFoundException(Exception):
    pass


class Item(object):
    ''' Given a JSON representation of an item, creates an Item object with
    parameters for each attribute of the item.
    '''
    item_types = {
        1: 'Magic',
        2: 'Rare',
        3: 'Unique',
        4: 'Gem',
    }

    socket_colors = {
        'S': 'R',
        'D': 'G',
        'I': 'B',
        'G': 'W',
    }

    def __init__(self, json):
        self.json = json
        self.parse_json()
        del self.json  # we're done with it at this point

    def parse_json(self):
        # easy stuff first
        self.verified = self.json.get('verified')
        self.corrupted = self.json.get('corrupted')
        self.image_url = self.json.get('icon')
        self.render_width = self.json.get('w') * 48  # pixels
        self.render_height = self.json.get('h') * 48  # pixels
        self.explicit_mods = self.json.get('explicitMods')

        # more complicated stuff
        self.detect_item_type()
        self.find_requirements()
        self.find_properties()
        self.find_sockets()

        # not implemented
        #self.identified = self.json.get('identified')
        #self.support = self.json.get('support')
        #self.socketed_items = self.json.get('socketedItems')

    def detect_item_type(self):
        ''' The "frameType" key seems to be what determines the type of an
        item. By detecting this early, we can save some headaches in finding
        the name and type of an item, because the data structures are not
        consistent. For example, rare items store their name in the "name"
        field, but gems store their name in the "typeLine" field.
        '''
        frame_type = self.json.get('frameType')
        self.item_type = Item.item_types.get(frame_type, 'Unknown')
        if self.item_type in ['Magic', 'Gem']:
            self.name = self.json.get('typeLine')
        else:
            self.name = self.json.get('name')
            self.item_base = self.json.get('typeLine')

    def find_requirements(self):
        ''' Level requirements, attribute requirements, etc.
        '''
        self.requirements = {}
        if 'requirements' in self.json:
            for requirement in self.json.get('requirements'):
                name, value = self.parse_values(requirement)
                self.requirements[name] = value

    def find_properties(self):
        ''' Implicit mods, mana multiplier for gems, etc.
        '''
        self.properties = {}
        if 'properties' in self.json:
            for property_json in self.json.get('properties'):
                if property_json.get('values'):  # if there are any values
                    name, value = self.parse_values(property_json)
                    self.properties[name] = value

    def find_sockets(self):
        ''' The sockets data is stored in the inverse way we want it. Sockets
        are listed with the group and attribute (str/dex/int) stored as values.
        This code maps sockets to groups (instead of groups to sockets),
        converts attributes to colors (RGB), and then uses some compaction to
        represent sockets and links with a single string, such as "R-G B B".
        '''
        if not self.json.get('sockets'):
            return
        socket_groups = {}
        for socket in self.json.get('sockets'):
            socket_group = socket.get('group')
            if socket_group not in socket_groups:
                socket_groups[socket_group] = []
            socket_color = Item.socket_colors.get(socket.get('attr'))
            socket_groups[socket_group].append(socket_color)

        # get the values (socket colors) while ignoring the socket group ids
        socket_groups = socket_groups.values()

        # show the largest groups of sockets first
        socket_groups = list(reversed(sorted(socket_groups, key=len)))

        # for each socket group, put the letters in the right order (R-G-B)
        socket_groups = [list(reversed(sorted(g))) for g in socket_groups]

        # compact the list down to a string
        # the inner join() connects linked sockets with hyphens
        # The outer join() connects socket groups with spaces
        # before compaction: [['R', 'G', 'B'], ['R', 'G'], ['R']]
        # after compaction: 'R-G-B R-G R'
        self.sockets = ' '.join(['-'.join(g) for g in socket_groups])

    def parse_values(self, json_struct):
        ''' Some of the JSON values are wacky data structures, like so:

            {u'name': 'Level', u'values': [[u'15', 0]]}

        This code parses out the name and value and returns a tuple. It needs
        to have more intelligence and be able to handle failures when the
        'values' key doesn't have this listception, but for now I've tried to
        handle these use cases before calling this function.
        '''
        name = json_struct.get('name')
        value = json_struct.get('values')[0][0]
        return (name, value)


def get_items(shop_thread_id):
    ''' Based on manual inspection, these seem to be the strings to the left
    and the right of the JSON list of items at the end of each shop thread in
    the forum. There may be a more reliable way to access this data.

    :param html: the html content of a forum shop thread
    :return: list of Item objects
    '''
    # get html
    url = 'http://www.pathofexile.com/forum/view-thread/%s' % shop_thread_id
    html = requests.get(url).content
    soup = BeautifulSoup(html)

    # find relevant javascript
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
    json_string = items_code.split(left_bound)[1].split(right_bound)[0]
    items_javascript = [entry[1] for entry in ujson.loads(json_string)]
    return [Item(i) for i in items_javascript]


def generate_html(shop_thread_id, items):
    try:
        template = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                searchpath=['pathofexile/forum/templates']
            )
        ).get_template('items.html')
    except Exception as e:
        logging.exception('Failed to load template: {}'.format(e.message))
    try:
        content = template.render(shop_thread_id=shop_thread_id, items=items)
        return content
    except Exception as e:
        logging.exception('Failed to render template: {}'.format(e.message))


def show_items(shop_thread_id):
    try:
        items = get_items(shop_thread_id)
    except Exception as e:
        logging.exception('Failed to retrieve items: {}'.format(e.message))
        error = '<p style="color:white">Shop thread {} contains no items!</p>'
        return error.format(shop_thread_id)
    return generate_html(shop_thread_id, items)
