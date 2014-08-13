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

Use `api.get_leagues()` to see all available leagues:

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
        ...  # returns up to 50 leagues
    ]

Leagues are accessed by their ID, which is a string:

    >>> hardcore_league = pathofexile.api.get_league('Hardcore')
    >>> print(hardcore_league)

    {
        u'description': u'A character killed in the Hardcore league is moved to the Standard league.',
        u'endAt': None,
        u'event': False,
        u'id': u'Hardcore',
        u'ladder': [],
        u'registerAt': None,
        u'rules': [
            {
                u'description': u'A character killed in Hardcore is moved to its parent league.',
                u'id': 4,
                u'name': u'Hardcore'
            }
        ],
        u'startAt': u'2013-01-23T21:00:00Z',
        u'url': u'http://www.pathofexile.com/forum/view-thread/71276'
    }  # returns only one league


League Rules
------------

Use `api.get_league_rules()` to see all available league rules:

    >>> import pathofexile.api
    >>> league_rules = pathofexile.api.get_league_rules()
    >>> print(league_rules)

    [
        {
            u'description': u'League requires a password to join.',
            u'id': 2,
            u'name': u'Private'
        },
        ...  # returns all possible league rules (10 as of August 2014)
    ]

League rules are accessed by their ID, which is an integer:

    >>> turbo_rule = pathofexile.api.get_league_rule(26)
    >>> print(turbo_rule)

    {
        u'description': u'Monsters move, attack and cast 60% faster.',
        u'id': u'26',
        u'name': u'Turbo'
    }  # returns only one league rule


Ladders
-------

The core API implementation offers two ways to retrieve the ladder for a given
league:

1. Request a segment of the ladder on top of each `get_league()` request
2. Request a ladder segment directly from the Ladder API endpoint

The first method is documented in the code, but is not recommended. The second
method works as follows:

    >>> import pathofexile.api
    >>> ladder_segment = pathofexile.api.get_ladder_segment('Standard', ladder_limit=20, ladder_offset=0)
    >>> print(ladder_segment)

    {
        u'entries': [
            {
                u'account': {
                    u'challenges': {
                        u'total': 0
                    },
                    u'name': u'Dawwwis'
                },
                u'character': {
                    u'class': u'Witch',
                    u'experience': 4250334444,
                    u'level': 100,
                    u'name': u'Em_Jake'
                },
                u'dead': False,
                u'online': False,
                u'rank': 1
            },
            ...  # returns 20 entries (set by ladder_limit)
        u'total': 15000
    }

The upstream API places an upper bound on the number of ladder entries we can
retrieve at once. The maximum is `200`, which is set by `ladder_limit`, and the
default is `20`. For a ladder of 15,000 players, this means we have to make 75
HTTP requests to pull down the entire ladder.

For the recommended way to retrieve an entire ladder at once, see the
<a href="ladders.md">Ladders</a> section of the documentation.
