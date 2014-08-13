pathofexile
===========

A Python framework for building tools related to Path of Exile.

Includes a complete implementation of the Path of Exile Developer API, tools
for analytics, and tools for forum scraping.

Pull requests are highly encouraged! If you see room for improvement, fork the
code, commit your patch, and then send a pull request so I can merge it in.


How The API Works <a name='howitworks'></a>
-----------------

Grinding Gear Games provides an official API for extracting data about leagues,
rules, and ladders in Path of Exile. You can see the documentation for this API
[here](http://www.pathofexile.com/developer/docs/api).

This code handles the retrieval of information from their API, and makes it
available as native Python data structures. This allows you to build tools on
top of this code which leverage the information from the API. If you're
programming in a language other than Python, you can use this as a reference
implementation.


Features <a name='features'></a>
--------
* Full implementation of the Path of Exile API
* Forum parsing code for shop threads
* Utilities to make pulling useful data faster and easier
* Pickle-based caching to avoid repeat lookups
* Analytics utilities for printing ladder statistics


Core API <a name='api'></a>
--------

Leagues: <a name='leagues'></a>


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

Ladders: <a name='ladders'></a>


    >>> import pathofexile.ladder
    >>> import pprint
    >>> ladder = pathofexile.ladder.retrieve('Standard')
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

Analytics: <a name='analytics'></a>


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


Forum Scraping <a name='forums'></a>
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
            u'icon': u'http://webcdn.pathofexile.com/image/Art/2DItems/Quivers/BlackgleamAlt.png',
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


Shop Thread Embeds
------------------

This part of the codebase allows you to isolate the first post of a shop thread
while retaining the CSS and Javascript responsible for style and functionality.

It was developed to allow iframe-style embeds on http://www.poearena.com.

The first part of this is the PostIsolator object, which scrapes the HTML of a
shop thread and parses it out:


    >>> import pathofexile.forum.posts
    >>> p = pathofexile.forum.posts.PostIsolator(516116)
    >>> p.html

        <complete html for the _first post only_ of shop thread 516116>

I've also included an application server which filters out posts when a request
is sent to `/shop/<thread_number>`, and returns the isolated HTML. It uses the
Flask application server and the gunicorn HTTP server.

To get started, you'll need to set up your virtualenv. Follow the
<a href="#dependencies">Installing Dependencies</a> section below. Then you can start
the server:

    $ bash post_server.sh

Once it's running, you can test it by hitting this url:

    http://<your server>:8080/shop/<thread_number>

You can then embed that URL as an iframe from another website, using HTML or
BBCode.


Installing Dependencies <a name='dependencies'></a>
-----------------------

Install virtualenv

    sudo pip install virtualenv

Create a virtualenv

    virtualenv env

Activate it

    source env/bin/activate

Install the Python library dependencies:

    pip install -r requirements.txt


To Do <a name='todo'></a>
-----

Documentation:

* Add general documentation for the included tools and their usage
* Add/expand in-code documentation (docstrings)

Core API:

* Use the documented return codes and error codes in the core API
  * Use the Codes.returns[429] error message when the rate limit is exceeded

Analytics:

* Add analytics for the number of ladder characters per account
  * 1 account has 5 ladder characters, 10 accounts have 4, etc.
* Write graph generation code for analytics
  * See http://i.imgur.com/lp0ZPCH.jpg

Forum Parsing:

* Continue to improve HTML/CSS/JS assets to improve visual style
  * See http://i.imgur.com/fOX0MFR.png

PVP:

* Write code to generate and manage tournament brackets
