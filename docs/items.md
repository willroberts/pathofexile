Items
=====

Relevant files:
* `pathofexile/forum/items.py`
* `pathofexile/forum/item_server.py`
* `pathofexile/forum/templates/items.html`
* `pathofexile/forum/assets/css/item_server.css`
* `item_server.sh`


Summary
-------

On the Path of Exile forums, shop threads include Javascript code which
contains a list of all items in the thread, as well as their metadata.

`items.py` is responsible for parsing the items from a shop thread, and it
returns them as a list of Item() objects. Item() is a custom class which
contains logic for parsing items, grouping sockets, resizing images, and more.

`item_server.py` is a small HTTP server which listens for requests to
`http://<server address>:8080/shop/<shop thread number>`, and then returns
rendered HTML content of the items in the requested thread. This HTML is
constructed and styled by `items.html` and `item_server.css`. To start the
server in the background, run `item_server.sh` when the virtualenv is active.


The Item() Class
----------------

Retrieve the items from a shop thread

    >>> import pathofexile.forum.items
    >>> items = pathofexile.forum.items.get_items(516116)
    >>> print len(items)

        173

Here's a sample item, and the attributes you can expect from the Item() class:

    >>> sample_item = items[100]
    >>> print sample_item
    <pathofexile.forum.items.Item object at 0x7feabb1c5e50>
    >>> print sample_item.__dict__

        {
            'corrupted': False,
            'explicit_mods': [
                u'144% increased Physical Damage',
                u'20% increased Attack Speed',
                u'+164 to Accuracy Rating',
                u'10% increased Movement Speed'
            ],
            'image_url': u'http://webcdn.pathofexile.com/image/Art/2DItems/Weapons/TwoHandWeapons/TwoHandSwords/TwoHandSword5Unique.png?scale=1&w=2&h=4&v=fb4f93392d82b1f9d21f9fa6236ac54f3',
            'item_base': u'Highland Blade',
            'item_type': 'Unique',
            'name': u"Rigvald's Charge",
            'properties': {
                u'Attacks per Second': u'1.44',
                u'Critical Strike Chance': u'5%',
                u'Physical Damage': u'122-224'
            },
            'render_height': 192,
            'render_width': 96,
            'requirements': {u'Dex': u'77', u'Level': u'44', u'Str': u'77'},
            'sockets': 'R-G G',
            'verified': True
        }
