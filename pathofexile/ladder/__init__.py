import grequests
import os
import time

try:
    import cPickle as pickle
except ImportError:
    import pickle

import pathofexile.api


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


def cache(original_function):
    ''' Checks for the existence of a recent cache file before retrieving a
    ladder from the API. Used when decorating retrieve() functions.

    If the cache file exists, returns the content of the cache file.
    Otherwise, makes the requests and saves the results to cache before
    returning control to the decorated function.

    :param original_function: the retrieve() function to be decorated
    '''
    def load_if_present(ladder_id, force_redownload=False):
        one_hour = 3600  # seconds
        cache_dir = '.ladder_cache'
        pickle_file = '{0}/{1}'.format(cache_dir, ladder_id.replace(' ', ''))

        # determine if loading from cache is an option
        if os.path.isfile(pickle_file) and not force_redownload:
            current_time = time.time()
            pickle_mtime = os.path.getmtime(pickle_file)

            # if the pickle file is less than one hour old, return the pickle
            if (current_time - pickle_mtime) < one_hour:
                with open(pickle_file, 'r') as f:
                    return pickle.load(f)

        ladder = original_function(ladder_id)
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)
        with open(pickle_file, 'w') as f:
            pickle.dump(ladder, f)
        return ladder

    return load_if_present


@cache
def retrieve_sequentially(ladder_id, force_redownload=False):
    ''' Makes 75 API requests to retrieve all 15,000 players in the given
    ladder. The average latency of a single response from the API is around
    1000ms, so this function takes about 75 seconds to complete.

    A better option is to retrieve the ladder concurrently with retrieve().

    :param ladder_id: The id (name) of the league for the ladder you want
        to retrieve.
    :param ladder_id: Name of the ladder to retrive (league name)
    :return: A list of all player details in the ladder
    '''
    entries = []
    ladder_size = 15000
    offset = 0
    limit = 200

    for _ in xrange(0, ladder_size, limit):
        p = pathofexile.api.get_ladder_segment(
            ladder_id,
            ladder_limit=limit,
            ladder_offset=offset
        )
        entries.extend(p.get('entries'))
        offset += limit

    return enries


@cache
def retrieve(ladder_id, force_redownload=False):
    ''' Uses concurrent HTTP requests to pull down a ladder. Takes roughly one
    quarter to one third of the time spent retrieving a ladder sequentially.

    A ladder contains 15,000 entries, and each request corresponds to 200 of
    those entries. Testing indicates that the API rate limit is 10 requests
    per second (defined in pathofexile.api), so we can send 8 groups of 10
    concurrent requests to get the entire ladder more quickly. Note: the last
    group only contains 5 requests (the remainder).

    The total time this function takes to complete should be around 20 seconds.
    Here's the breakdown of what makes this take so long:

        * 0.5 seconds: Python code
        * 7.0 seconds: time.sleep() - once between each request group
        * 12.5 seconds: Latency for 8 request groups

    The request latency is time spent waiting on a response from the API. The
    latency for a request can vary from 800ms to 3400ms (requests appear to be
    a bit slower when sent in batches like this). 1500ms seems to be the
    average latency for a request group. The slowest request in a group
    determines the latency of its group.

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
        # generate the request objects
        requests.append(grequests.get(endpoint, params=params))
        offset += limit

    # Make 75 requests, 10 at a time
    chunks = create_chunks(requests, pathofexile.api.RATE_LIMIT)
    entries = []
    for chunk in chunks:
        # send the requests
        responses = grequests.map(chunk)
        for r in responses:
            entry_group = r.json().get('entries')
            entries.extend(entry_group)
        # only sleep if we'll be making more requests
        if not len(entries) == 15000:
            time.sleep(1)
    return entries
