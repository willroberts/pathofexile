import grequests
import sys
import time

import pathofexile.api

'''
Path of Exile API Client
- Wrapper functions for the API implementation
'''


def create_chunks(l, n):
    ''' Yield successive n-sized chunks from l.

    :param l: any list object
    :param n: split the list object into lists of this size
    :return: generator of list 'chunks'
    '''
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def make_batch_request(requests):
    ''' Maps each given request to a response, and returns a list of the
    responses.

    :param requests: list of request objects
    :return: list of response objects
    '''
    responses = []
    responses.extend(grequests.map(requests))
    return responses


def get_ladder_sequentially(ladder_id):
    ''' Makes 75 API requests to retrieve all 15,000 players in the given
    ladder.

    :param ladder_id: The id (name) of the league for the ladder you want
    to retrieve.

    :param ladder_id: Name of the ladder to retrive (league name)
    :return: A list of all player details in the ladder
    '''
    players = []
    ladder_size = 15000
    offset = 0
    limit = 200

    for _ in xrange(0, ladder_size, limit):
        p = pathofexile.api.get_ladder(
            ladder_id,
            ladder_limit=limit,
            ladder_offset=offset
        )
        players.extend(p.get('entries'))
        offset += limit

    return players


def get_ladder_concurrently(ladder_id):
    ''' Testing indicates that the API allows 10 concurrent requests at a given
    time. This may be requests per second.

    :param ladder_id: Name of the ladder to retrive (league name)
    :return: list of ladder entries
    '''
    ladder_size = 15000
    limit = 200
    offset = 0
    endpoint = 'http://api.pathofexile.com/ladders'

    # Prepare 75 requests
    requests = []
    while offset != ladder_size:
        params = {'id': ladder_id, 'limit': limit, 'offset': offset}
        requests.append(grequests.get(endpoint, params=params))
        offset += limit

    # Make 75 requests, 5 at a time
    chunks = create_chunks(requests, 5)
    entries = []
    for chunk in chunks:
        responses = grequests.map(chunk)
        for r in responses:
            entry_group = r.json().get('entries')
            entries.extend(entry_group)
        time.sleep(0.5)  # 10 requests per second

    return entries
