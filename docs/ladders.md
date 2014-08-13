Ladders
=======

Relevant files:
* `pathofexile/ladders/__init__.py`


Summary
-------

The Path of Exile API limits ladder retrievals to 200 entries per request,
which means we need to send 75 requests to retrieve the entire ladder.

In order to make this faster, we use the
<a href="https://github.com/kennethreitz/grequests">grequests</a> library for
concurrent HTTP request mapping.

The API seems to accept around 10 requests per second before triggering rate
limits, so we call `sleep()` between each batch of requests to avoid being
rate limited. It takes around 20 seconds to retrieve a ladder in this way,
depending on the latency of responses from api.pathofexile.com.

The ladder is cached to disk locally after the first ladder retrieval, so
subsequent lookups will be nearly instantaneous. The cache is preferred if it
is less than one hour old, but an update can be forced by passing
`force_redownload=True` into the `retrieve()` function. For more information
on the caching system, see the `cache()` decorator function.


Retrieving A Ladder
-------------------

    >>> import pathofexile.ladder
    >>> import pprint
    >>> ladder = pathofexile.ladder.retrieve('Standard')
    >>> pprint.pprint(ladder)

    [
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
            u'rank': 1,
        },
        ...  # returns all 15,000 ladder entries
    ]
