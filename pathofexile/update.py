import os
import pickle
import time

import pathofexile.api
import pathofexile.utilities

'''
Path of Exile API Client
- Updates (Retrievals, Caching, etc.)
- Implementations of functions defined in pathofexile.api
'''


def get_ladder(league, force_update=False):
    ''' Get all players from a ladder concurrently. Delays requests to avoid
    being rate limited.

    :param league: Name of the league
    :param force_update: boolean to bypass caching/pickling
    :return: dict object from API JSON response
    '''
    pickle_file = 'cache/%s' % (league.replace(' ', ''))
    if os.path.isfile(pickle_file) and not force_update:
        current_time = time.time()
        pickle_time = os.path.getmtime(pickle_file)

        # if the pickle file is less than one day old, return the pickle
        if (current_time - pickle_time) < 86400:
            with open(pickle_file, 'r') as f:
                return pickle.load(f)

    # otherwise, retrieve the ladder and then cache it locally
    print 'Retrieving new ladder for \'%s\'. This can take up to a minute.' % (
        league,
    )
    ladder = pathofexile.utilities.get_ladder_concurrently(league)
    with open(pickle_file, 'w') as f:
        pickle.dump(ladder, f)
    return ladder


def list_leagues(names_only=True, races_only=False):
    ''' Returns up to 50 leagues.

    :param names_only: Only include league names, as opposed to the entire
        JSON structure of league metadata
    :param races_only: Only include event leagues
    :return: List of league names or data structures
    '''
    if races_only:
        league_type = 'event'
    else:
        league_type = 'all'
    leagues = pathofexile.api.list_leagues(league_type=league_type)
    if names_only:
        return [l.get('id') for l in leagues]
    return leagues


def get_league_details(league):
    ''' Retrieves the details for a given league, including rule set.

    :param league: League for which to retrieve details
    :return: dict of API JSON response
    '''
    return pathofexile.api.get_league(league)


def get_league_rules():
    ''' Retrieves all available league rules.
    :return: dict of API JSON response
    '''
    return pathofexile.api.list_league_rules()


def get_league_rule(league_rule_id):
    ''' Retrieves the details for a given league rule.

    :param league_rule_id: int ID of the desired league rule
    :param return: dict of API JSON response
    '''
    return pathofexile.api.get_league_rule(league_rule_id)
