pathofexile
===========

A Python framework for building tools related to Path of Exile.

Includes a complete implementation of the Path of Exile Developer API, tools
for analytics, and tools for forum scraping.

Pull requests are highly encouraged! If you see room for improvement, fork the
code, commit your patch, and then send a pull request so I can merge it in.


How The API Works
-----------------

Grinding Gear Games provides an official API for extracting data about leagues,
rules, and ladders in Path of Exile. You can see the documentation for this API
[here](http://www.pathofexile.com/developer/docs/api).

This code handles the retrieval of information from their API, and makes it
available as native Python data structures. This allows you to build tools on
top of this code which leverage the information from the API. If you're
programming in a language other than Python, you can use this as a reference
implementation.


Core API
--------

Leagues:


    >>> import pathofexile.api
    >>> import pprint
    >>> leagues = pathofexile.api.list_leagues()
    >>> pprint.pprint(leagues)

    [{u'description': u'The default game mode.',
      u'endAt': None,
      u'event': False,
      u'id': u'Standard',
      u'ladder': [],
      u'registerAt': None,
      u'rules': [],
      u'startAt': u'2013-01-23T21:00:00Z',
      u'url': u'http://www.pathofexile.com/forum/view-thread/71278',
     },
     ...
    ]

Ladders:


    >>> import pathofexile.utilities
    >>> import pprint
    >>> ladder = pathofexile.utilities.cache_ladder('Standard')
    >>> pprint.pprint(ladder)

    [{u'account': {u'challenges': {u'total': 0}, u'name': u'Dawwwis'},
      u'character': {u'class': u'Witch',
                     u'experience': 4250334444,
                     u'level': 100,
                     u'name': u'Em_Jake'},
      u'dead': False,
      u'online': False,
      u'rank': 1,
     },
     ...
    ]

Analytics:


    >>> import pathofexile.analytics
    >>> pathofexile.analytics.report('Standard')

    Standard
    ********
    Have Twitch accounts: 2501 (16.67%)
    Online (19:00 UTC): 445 (2.97%)
    Level breakdown:
        80+: 6996 (46.64%)
        90+: 7937 (52.91%)
        100+: 67 (0.45%)
    Class breakdown:
        Scion: 2772 (18.48%)
        Templar: 1003 (6.69%)
        Ranger: 2015 (13.43%)
        Witch: 2842 (18.95%)
        Duelist: 1804 (12.03%)
        Shadow: 1487 (9.91%)
        Marauder: 3077 (20.51%)
    Challenge completion breakdown:
        0 challenges completed: 7864 (52.43%)
        1 challenges completed: 3184 (21.23%)
        2 challenges completed: 1546 (10.31%)
        3 challenges completed: 935 (6.23%)
        4 challenges completed: 642 (4.28%)
        5 challenges completed: 453 (3.02%)
        6 challenges completed: 204 (1.36%)
        7 challenges completed: 136 (0.91%)
        8 challenges completed: 36 (0.24%)


Forum Scraping
--------------

Retrieving items from shop threads:


    >>> import pathofexile.forum
    >>> import pprint
    >>> items = pathofexile.forum.find_items(923014)
    >>> pprint.pprint(items)
    
    [
        {
            u'corrupted': False,
            u'explicitMods': [
                u'10% increased Attack Speed',
                u'+20 to Evasion Rating',
                u'+23 to maximum Mana',
                u'42% of Physical Damage Converted to Fire Damage'
            ],
            u'flavourText': [
                u'Molten feathers, veiled spark,\r',
                u'Hissing arrows from the dark.'
            ],
            u'frameType': 3,
            u'h': 3,
            u'icon': u'http://webcdn.pathofexile.com/image/Art/2DItems/Quivers/BlackgleamAlt.png?scale=1&w=2&h=3&v=b663d1bf51f5acb8518da43063c1a5df3',
            u'identified': True,
            u'implicitMods': [
                u'Adds 4-8 Fire Damage to attacks with Bows'
            ],
            u'league': u'Unknown',
            u'name': u'Blackgleam',
            u'requirements': [
                {
                    u'displayMode': 0,
                    u'name': u'Level',
                    u'values': [
                        [
                            u'22',
                            0
                        ]
                    ]
                }
            ],
            u'socketedItems': [],
            u'sockets': [],
            u'support': True,
            u'typeLine': u'Fire Arrow Quiver',
            u'verified': True,
            u'w': 2
        },
        ...
    ]


Features
--------
* Full implementation of the PoE API
* Utilities to make pulling useful data easier
* Concurrent request mapping to speed up retrieval
* Pickle-based caching to avoid repeat lookups
* Analytics utilities for printing ladder statistics


Installing Dependencies
-----------------------

Install virtualenv

    sudo pip install virtualenv

Create a virtualenv

    virtualenv env

Activate it

    source env/bin/activate

Install the Python library dependencies:

    pip install -r requirements.txt

