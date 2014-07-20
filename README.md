pathofexile
===========

A Python client for the Path of Exile Developer API. Includes some analytics
tools and pickle-based caching.

Grinding Gear Games provides an official API for extracting data about leagues,
rules, and ladders in Path of Exile. You can see the documentation for this API
[here](http://www.pathofexile.com/developer/docs/api).

This code handles the retrieval of information from their API, and makes it
available as native Python data structures. This allows you to build tools on
top of this code which leverage the information from the API. If you're
programming in a language other than Python, you can use this as a reference
implementation.

Pull requests are highly encouraged! If you see room for improvement, fork the
code, commit your patch, and then send a pull request so I can merge it in.


Getting Started / Sample Usage
------------------------------

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

    >>> import pathofexile.update
    >>> import pathofexile.analytics
    >>> ladder = pathofexile.update.get_ladder('Standard')
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


Features
--------
* Full implementation of the PoE API
* Utilities to make pulling useful data easier
* Concurrent request mapping to speed up retrieval
* Pickle-based caching to avoid repeat lookups
* Analytics utilities for printing ladder statistics


Coming Soon / To Do
-------------------
* RRD storage and graphing for online player counts
* Simplification of the codebase (will probably remove update.py)
* Caching improvements
* Improvements to ladder retrieval speed


Installing Dependencies
-----------------------

If you're on Ubuntu Linux, install the dependency packages:

    sudo apt-get install libxml2-dev libcairo2-dev python-cairo-dev libpango1.0-dev librrd-dev

Install virtualenv

    sudo pip install virtualenv

Create a virtualenv

    virtualenv env

Activate it

    source env/bin/activate

Install the Python library dependencies:

    pip install -r requirements.txt

