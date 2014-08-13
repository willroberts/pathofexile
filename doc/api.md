Core API Documentation
======================

Relevant files:

* pathofexile/api.py

Summary
-------

Grinding Gear Games provide a JSON API for retrieving information about
leagues, league rules, and ladders from http://api.pathofexile.com.

The full documentation for the official Path of Exile API can be found here:
http://www.pathofexile.com/developer/docs/api

This code (api.py) provides a client library for retrieving the API data and
converting it into native Python data structures (dictionaries and lists).

Leagues
-------

    >>> import pathofexile.api
    >>> leagues = pathofexile.api.get_leagues()
    >>> print(leagues)

    [
        {
            u'description': u'The default game mode.',
            u'endAt': None,
            u'event': False,
            u'id': u'Standard',
            u'ladder': [],
            u'registerAt': None,
            u'rules': [],
            u'startAt': u'2013-01-23T21:00:00Z',
            u'url': u'http://www.pathofexile.com/forum/view-thread/71278',
        },
        ...  (contains up to 50 leagues)
    ]


League Rules
------------


Ladders
-------

    >>> import pathofexile.ladder
    >>> ladder = pathofexile.ladder.retrieve('Standard')
    >>> print(ladder)

    [
        {
            u'account': {
                u'challenges': {
                    u'total': 0
                },
                u'name':
                u'Dawwwis'
            },
            u'character': {
                u'class': u'Witch',
                u'experience': 4250334444,
                u'level': 100,
                u'name': u'Em_Jake'
            },
            u'dead': False,
            u'online': False,
            u'rank': 1,
        },
        ...  (contains up to 15,000 entries)
    ]

